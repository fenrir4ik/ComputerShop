from django.core.validators import MinValueValidator
from django.db import models


class Vendor(models.Model):
    class Meta:
        db_table = 'vendor'

    name = models.CharField(max_length=50, unique=True)
    #add more info about vendor

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

    image = models.ImageField(upload_to='product', default='product/default_product.png', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)


class ProductPrice(models.Model):
    class Meta:
        db_table = 'product_price'

    price = models.DecimalField(decimal_places=2, max_digits=11, validators=[MinValueValidator(0.01)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_actual = models.DateTimeField(auto_now_add=True)
