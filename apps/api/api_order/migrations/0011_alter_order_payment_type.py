# Generated by Django 3.2.9 on 2021-12-09 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_order', '0010_order_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='api_order.paymenttype'),
        ),
    ]