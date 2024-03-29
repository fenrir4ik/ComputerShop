from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, patronymic, phone_number, password=None):
        if not email:
            raise ValueError("User should have an email address.")
        if not name:
            raise ValueError("User should have a name.")
        if not surname:
            raise ValueError("User should have a surname.")
        if not patronymic:
            raise ValueError("User should have a patronymic.")

        user = self.model(
            email=self.normalize_email(email),
            name=name.capitalize(),
            surname=surname.capitalize(),
            patronymic=patronymic.capitalize(),
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, patronymic, phone_number=None, password=None):
        user = self.create_user(email, name, surname, patronymic, phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True, db_index=True)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    patronymic = models.CharField(max_length=45)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'patronymic']

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f'{self.name} {self.surname} {self.patronymic}'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
