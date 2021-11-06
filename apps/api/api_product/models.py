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

    char_name = models.CharField(max_length=100)
    char_value = models.CharField(max_length=100)


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

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    product_vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT)
    product_characteristics = models.ManyToManyField(Characteristics, through='ProductCharacteristics')
    product_name = models.CharField(max_length=100, db_index=True)
    product_price = models.DecimalField(decimal_places=2,max_digits=9)
    product_amount = models.PositiveIntegerField()
    product_description = models.TextField()
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.product_name


    def delete(self, using=None, keep_parents=False):
        self.product_image.storage.delete(self.product_image.name)
        super().delete()


class ProductCharacteristics(models.Model):
    class Meta:
        db_table = 'product_chars'

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    chars = models.ForeignKey(Characteristics, on_delete=models.CASCADE)


@receiver(pre_save, sender=Product)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        product = Product.objects.get(pk=instance.pk)
        if instance.product_image and product.product_image != instance.product_image:
            product.product_image.delete(False)