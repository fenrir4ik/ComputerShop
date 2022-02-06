from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

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
        return f'{self.name} [{self.amount}]'


class ProductImage(models.Model):
    class Meta:
        db_table = 'product_image'

    image = models.ImageField(upload_to='product', default=DEFAULT_PRODUCT_IMAGE, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.image}, {self.product}, is_main: {self.is_main}'


class ProductPrice(models.Model):
    class Meta:
        db_table = 'product_price'

    price = models.DecimalField(decimal_places=2, max_digits=11, validators=[MinValueValidator(0.00)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_actual = models.DateTimeField(auto_now_add=True)


@receiver(post_delete, sender=ProductImage)
def delete_image_from_storage(sender, instance, *args, **kwargs):
    product_image = ProductImage.objects.filter(pk=instance.pk).exists()
    if instance.pk and not product_image and instance.image != DEFAULT_PRODUCT_IMAGE:
        instance.image.delete(False)
