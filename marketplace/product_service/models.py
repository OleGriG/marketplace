from django.db import models

from user_service.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="имя категории",
        unique=True
    )
    # TODO: добавить фотку и минио

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category_table'
        verbose_name = 'Категория'


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(
        max_length=200,
        verbose_name='имя продукта'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    display_on_main_page = models.BooleanField(
        verbose_name="показывать на главной странице?",
        default=False
    )
    # TODO: добавить фотки и минио

    def __str__(self):
        return self.name
