# Generated by Django 3.2.9 on 2022-01-31 18:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'vendor',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('amount', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='store.category')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='store.vendor')),
            ],
            options={
                'db_table': 'product',
            },
        ),
    ]