# Generated by Django 3.2.9 on 2021-11-07 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_product', '0012_remove_characteristics_char_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcharacteristics',
            name='char_value',
            field=models.CharField(default=3200, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='char_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]