# Generated by Django 4.0.2 on 2022-02-06 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_productimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, default='product/default_product.png', upload_to='product'),
        ),
    ]
