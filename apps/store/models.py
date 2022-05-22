from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone

from apps.core.models import User
from services.settings import DEFAULT_PRODUCT_IMAGE
from services.recommender_service import RecommenderService


class Country(models.Model):
    name = models.CharField(max_length=60, unique=True)

    class Meta:
        db_table = 'country'


class Vendor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = models.CharField(max_length=12, unique=True, db_index=True)
    postal_code = models.CharField(max_length=12, db_index=True)
    description = models.TextField(verbose_name="Описание")
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)

    class Meta:
        db_table = 'vendor'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class Characteristic(models.Model):
    name = models.CharField(verbose_name="Название характеристики", max_length=50, unique=True)

    class Meta:
        db_table = 'characteristic'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название", db_index=True)
    amount = models.PositiveIntegerField(verbose_name="Количество", default=0)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.RESTRICT)
    vendor = models.ForeignKey(Vendor, related_name='products', verbose_name="Производитель", on_delete=models.RESTRICT)
    date_created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    description = models.TextField(verbose_name="Описание")
    characteristics = models.ManyToManyField(Characteristic, related_name='products', through='ProductCharacteristic')
    reviews = models.ManyToManyField(User, through='Review')
    rating = models.DecimalField(decimal_places=6, max_digits=16, default=0)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return f'Product[{self.pk}], {self.name=}, {self.amount=}'


class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    characteristic = models.ForeignKey(Characteristic, related_name='char_item', on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=50)

    class Meta:
        db_table = 'product_characteristic'
        unique_together = ('product', 'characteristic')

    def __str__(self):
        return f"{self.characteristic.name}: {self.value}"


class ProductImage(models.Model):
    image = models.ImageField(verbose_name='Изображение', upload_to='product', default=DEFAULT_PRODUCT_IMAGE,
                              blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)

    class Meta:
        db_table = 'product_image'

    def __str__(self):
        return f'ProductImage[{self.pk}], {self.image=}, {self.product_id=}, {self.is_main=}'


class ProductPrice(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=11, validators=[MinValueValidator(0.00)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_actual = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_price'

    def __str__(self):
        return f'ProductPrice {self.date_actual}, {self.price}'


class PaymentType(models.Model):
    type = models.CharField(max_length=50, db_index=True, unique=True)

    class Meta:
        db_table = 'payment_type'

    def __str__(self):
        return self.type


class OrderStatus(models.Model):
    name = models.CharField(verbose_name="Статус", max_length=50, db_index=True, unique=True)

    class Meta:
        db_table = 'order_status'

    def __str__(self):
        return self.name

    @classmethod
    def retrieve_id(cls, status_name: str):
        status_dict = {
            "new": 1,  # Ожидает подтверждения
            "confirmed": 2,  # "Подтвержден"
            "packed_up": 3,  # "Комплектуется"
            "on_way": 4,  # "Следует в город получателя"
            "at_post": 5,  # "Находится в почтовом отделении"
            "completed": 6,  # "Выполнен"
            "canceled": 7,  # "Отменен"
            "not_picked": 8,  # "Получатель не забрал заказ"
            "in_shop": 9,  # "Находится в магазине"
        }
        return status_dict.get(status_name)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    status = models.ForeignKey(OrderStatus, on_delete=models.RESTRICT, verbose_name="Статус", blank=True, null=True)
    payment = models.ForeignKey(PaymentType, on_delete=models.RESTRICT, verbose_name="Способ оплаты", null=True)
    products = models.ManyToManyField(Product, through='CartItem')
    name = models.CharField(max_length=45, verbose_name="Имя", null=True)
    surname = models.CharField(max_length=45, verbose_name="Фамилия", null=True)
    patronymic = models.CharField(max_length=45, verbose_name="Отчество", null=True)
    phone_number = models.CharField(max_length=12, verbose_name="Номер телефона", db_index=True, null=True)
    email = models.CharField(max_length=255, verbose_name="Электронная почта", db_index=True, null=True)
    date_start = models.DateTimeField(blank=True, verbose_name="Дата создания заказа", null=True)
    date_end = models.DateTimeField(blank=True, verbose_name="Дата завершения заказа", null=True)
    address = models.CharField(max_length=255, verbose_name="Адрес доставки", blank=True, null=True)

    class Meta:
        db_table = 'order'

    def __str__(self):
        return f'Order[{self.pk}], {self.user_id=}, {self.status=}, {self.date_start=}, {self.date_end=}'

    def save(self, *args, **kwargs):
        if self.status_id == OrderStatus.retrieve_id('completed') and not self.date_end:
            self.date_end = timezone.now()
            super().save(*args, **kwargs)
            RecommenderService().process_cart_items(self.pk)
        else:
            super().save(*args, **kwargs)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        db_table = 'cart_item'
        unique_together = ('product', 'order')

    constraints = [
        models.CheckConstraint(check=models.Q(amount__gte=1), name='amount_positive'),
    ]


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)

    class Meta:
        db_table = 'review'


@receiver(post_delete, sender=ProductImage)
def delete_image_from_storage(sender, instance, *args, **kwargs):
    product_image = ProductImage.objects.filter(pk=instance.pk).exists()
    if instance.pk and not product_image and instance.image != DEFAULT_PRODUCT_IMAGE:
        instance.image.delete(False)

