from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class ProductType(models.Model):
    class Meta:
        db_table = 'product_type'

    type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.type_name


class Characteristics(models.Model):
    class Meta:
        db_table = 'characteristics'

    char_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.char_name}"


class Country(models.Model):
    class Meta:
        db_table = 'country'

    country_name = models.CharField(max_length=100)

    def __str__(self):
        return self.country_name


class Vendor(models.Model):
    class Meta:
        db_table = 'vendor'

    vendor_country = models.ForeignKey(Country, on_delete=models.RESTRICT)
    vendor_email = models.EmailField(db_index=True)
    vendor_description = models.TextField()
    vendor_name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.vendor_name


class Product(models.Model):
    class Meta:
        db_table = 'product'
        constraints = [
            models.CheckConstraint(check=models.Q(product_price__gte='0'), name='product_price_non_negative'),
        ]

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    product_vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT, related_name='products')
    product_characteristics = models.ManyToManyField(Characteristics, related_name='products', through='ProductCharacteristics')
    product_name = models.CharField(max_length=100, db_index=True)
    product_price = models.DecimalField(decimal_places=2, max_digits=9)
    product_amount = models.PositiveIntegerField()
    product_description = models.TextField()
    product_image = models.ImageField(upload_to='product', default='product/default.png', blank=True)

    def __str__(self):
        return self.product_name


    def delete(self, using=None, keep_parents=False):
        self.product_image.storage.delete(self.product_image.name)
        super().delete()


class ProductCharacteristics(models.Model):
    class Meta:
        db_table = 'product_chars'
        unique_together = (('product', 'char', 'char_value'),)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    char = models.ForeignKey(Characteristics, on_delete=models.CASCADE)
    char_value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.char.char_name}: {self.char_value}"


@receiver(pre_save, sender=Product)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        product = Product.objects.get(pk=instance.pk)
        if instance.product_image \
                and product.product_image != instance.product_image \
                and product.product_image.name != 'default.png':
            product.product_image.delete(False)
