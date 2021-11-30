# Generated by Django 3.2.9 on 2021-11-29 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_email',
            field=models.CharField(blank=True, db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_name',
            field=models.CharField(blank=True, db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_surname',
            field=models.CharField(blank=True, db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_telno',
            field=models.CharField(blank=True, db_index=True, max_length=30),
        ),
    ]