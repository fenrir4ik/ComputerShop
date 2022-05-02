# Generated by Django 4.0.2 on 2022-04-12 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_country_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='store.country'),
            preserve_default=False,
        ),
    ]
