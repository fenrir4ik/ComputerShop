# Generated by Django 4.0.2 on 2022-03-30 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_order_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Characteristic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название характеристики')),
            ],
            options={
                'db_table': 'characteristic',
            },
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='name',
            field=models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='product',
            name='amount',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(default='product/default_product.png', upload_to='product', verbose_name='Изображение'),
        ),
        migrations.CreateModel(
            name='ProductCharacteristic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=50, verbose_name='Значение')),
                ('characteristics', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.characteristic')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'db_table': 'product_characteristic',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='characteristics',
            field=models.ManyToManyField(related_name='products', through='store.ProductCharacteristic', to='store.Characteristic'),
        ),
    ]
