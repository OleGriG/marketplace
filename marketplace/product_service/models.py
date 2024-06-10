from django.db import models

from user_service.models import User, Seller


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
        Seller,
        on_delete=models.CASCADE,
        null=True
    )
    display_on_main_page = models.BooleanField(
        verbose_name="показывать на главной странице?",
        default=False
    )
    price = models.IntegerField(
        verbose_name="Цена",
        default=0
    )
    rate = models.FloatField(
        verbose_name="Рейтинг товара",
        default=0
    )
    main_photo = models.ImageField(
        verbose_name=' главная фотография',
        upload_to='product_photos/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class ProductPhoto(models.Model):
    photo = models.ImageField(
        verbose_name='фотография',
        upload_to='product_photos/'
    )
    product = models.ForeignKey(
        Product,
        verbose_name='продукт',
        on_delete=models.CASCADE
    )


class Slider(models.Model):
    photo = models.ImageField(
        verbose_name='фотография',
        upload_to='product_photos/'
    )


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="user",
        unique=True
    )
    products = models.ManyToManyField(
        Product,
        blank=True
    )
