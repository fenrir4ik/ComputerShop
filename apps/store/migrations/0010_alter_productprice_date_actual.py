# Generated by Django 4.0.2 on 2022-02-04 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productprice',
            name='date_actual',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]