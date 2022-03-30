# Generated by Django 4.0.2 on 2022-03-30 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_characteristics_productcharacteristic_characteristic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcharacteristic',
            name='characteristic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='char_item', to='store.characteristic'),
        ),
    ]
