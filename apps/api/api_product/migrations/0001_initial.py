# Generated by Django 3.2.9 on 2021-11-06 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Characteristics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char_name', models.CharField(max_length=100)),
                ('char_value', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'characteristics',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('product_amount', models.PositiveIntegerField()),
                ('product_description', models.TextField()),
                ('product_image', models.ImageField(upload_to='')),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'product_type',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_email', models.EmailField(max_length=254)),
                ('vendor_description', models.TextField()),
                ('vendor_name', models.CharField(max_length=100)),
                ('vendor_country', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api_product.country')),
            ],
            options={
                'db_table': 'vendor',
            },
        ),
        migrations.CreateModel(
            name='ProductCharacteristics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chars', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_product.characteristics')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_product.product')),
            ],
            options={
                'db_table': 'product_chars',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_characteristics',
            field=models.ManyToManyField(through='api_product.ProductCharacteristics', to='api_product.Characteristics'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api_product.producttype'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api_product.vendor'),
        ),
    ]
