# Generated by Django 4.0.1 on 2022-01-17 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(db_index=True, max_length=12, null=True),
        ),
    ]