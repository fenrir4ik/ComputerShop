# Generated by Django 4.0.2 on 2022-03-03 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True)),
                ('phone_number', models.CharField(blank=True, db_index=True, max_length=12, null=True)),
                ('name', models.CharField(max_length=45)),
                ('surname', models.CharField(max_length=45)),
                ('patronymic', models.CharField(max_length=45)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now=True)),
                ('role', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Manager'), (2, 'Warehouse worker')], null=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(('role__in', [1, 2])), name='valid_role'),
        ),
    ]
