# Generated by Django 4.0.2 on 2022-02-16 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_remove_order_customer_email_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product',
            new_name='products',
        ),
    ]
