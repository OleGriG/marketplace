from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields = {"is_staff": False, "is_superuser": False, **extra_fields}
        if not email:
            raise ValueError("Users must have an email address")

        user = User(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            raise ValueError("Users must have an password")
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields = {**extra_fields, "is_staff": True, "is_superuser": True}
        user = self.create_user(email=email, password=password, **extra_fields)
        return user


class User(AbstractUser):
    """Model of User"""
    class UserStatus(models.TextChoices):
        VERIFIED = 'VE', _("Подтвержденный")
        NOT_VERIFIED = 'NE', _("Не подтсвержденный")
        BANNED = 'BA', _("Заблокированный")

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    first_name = models.CharField(
        max_length=200,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name="Фамилия"
    )
    email = models.EmailField(
        unique=True,
        max_length=200,
        verbose_name="почта"
    )
    status = models.CharField(
        max_length=2, choices=UserStatus,
        default=UserStatus.NOT_VERIFIED, verbose_name='Статус'
    )
    is_saller = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        db_table = 'users_table'

    def __str__(self):
        return f'{self.email}, {self.first_name}'
