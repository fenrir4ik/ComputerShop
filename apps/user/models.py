from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, patronymic, phone_number, password=None):
        pass

    def create_superuser(self, email, name, surname, patronymic, phone_number, password=None):
        pass


class User(AbstractBaseUser):
    class Meta:
        db_table = 'user'

    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    patronymic = models.CharField(max_length=45)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'patronymic', 'phone_number']

    def __str__(self):
        return f'User {self.email} {self.phone_number}'
