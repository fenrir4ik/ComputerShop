# Generated by Django 3.2.9 on 2021-11-12 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_product', '0020_alter_product_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, default='product/default.png', upload_to='product'),
        ),
    ]
