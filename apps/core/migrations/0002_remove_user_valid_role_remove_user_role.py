# Generated by Django 4.0.2 on 2022-04-11 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='user',
            name='valid_role',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
    ]
