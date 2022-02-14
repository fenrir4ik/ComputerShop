from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.user.models import User
from computershop.settings import DEFAULT_PRODUCT_IMAGE


class Vendor(models.Model):
    class Meta:
        db_table = 'vendor'

    name = models.CharField(max_length=50, unique=True)

    # add more info about vendor

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        db_table = 'category'

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        db_table = 'product'

    name = models.CharField(max_length=255, db_index=True)
    amount = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f'Product[{self.pk}], {self.name=}, {self.amount=}'


class ProductImage(models.Model):
    class Meta:
        db_table = 'product_image'

    image = models.ImageField(upload_to='product', default=DEFAULT_PRODUCT_IMAGE, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f'ProductImage[{self.pk}], {self.image=}, {self.product_id=}, {self.is_main=}'


class ProductPrice(models.Model):
    class Meta:
        db_table = 'product_price'

    price = models.DecimalField(decimal_places=2, max_digits=11, validators=[MinValueValidator(0.00)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_actual = models.DateTimeField(auto_now_add=True)


class PaymentType(models.Model):
    class Meta:
        db_table = 'payment_type'

    type = models.CharField(max_length=50, db_index=True, unique=True)

    def __str__(self):
        return self.type


class OrderStatus(models.Model):
    class Meta:
        db_table = 'order_status'

    name = models.CharField(max_length=50, db_index=True, unique=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    class Meta:
        db_table = 'order'

    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    status = models.ForeignKey(OrderStatus, on_delete=models.RESTRICT, blank=True, null=True)
    payment = models.ForeignKey(PaymentType, on_delete=models.RESTRICT, null=True)
    product = models.ManyToManyField(Product, related_name='Orders', through='CartItem')
    customer_name = models.CharField(max_length=45, null=True)
    customer_surname = models.CharField(max_length=45, null=True)
    customer_patronymic = models.CharField(max_length=45, null=True)
    customer_phone_number = models.CharField(max_length=12, null=True, db_index=True)
    customer_email = models.CharField(max_length=255, unique=True, db_index=True, null=True)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    address = models.TextField(null=True)

    def __str__(self):
        return f'Order[{self.pk}], {self.user_id=}, {self.status=}, {self.date_start=}, {self.date_end=}'


class CartItem(models.Model):
    class Meta:
        db_table = 'cart_item'

    constraints = [
        models.CheckConstraint(check=models.Q(amount__gte=1), name='amount_positive'),
    ]

    unique_together = (('product', 'order'), )

    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()


@receiver(post_delete, sender=ProductImage)
def delete_image_from_storage(sender, instance, *args, **kwargs):
    product_image = ProductImage.objects.filter(pk=instance.pk).exists()
    if instance.pk and not product_image and instance.image != DEFAULT_PRODUCT_IMAGE:
        instance.image.delete(False)
