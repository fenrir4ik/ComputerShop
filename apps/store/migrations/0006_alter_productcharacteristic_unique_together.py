# Generated by Django 4.0.2 on 2022-03-30 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_productcharacteristic_characteristic'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productcharacteristic',
            unique_together={('product', 'characteristic')},
        ),
    ]
