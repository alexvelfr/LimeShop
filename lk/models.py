from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(verbose_name='Номер телефона', unique=True, blank=True, max_length=20)


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=150, unique=True, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='Название товара', max_length=150, unique=True, blank=False)
    category = models.ForeignKey(ProductCategory, verbose_name='Категория', related_name='category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductSeries(models.Model):
    number = models.IntegerField(verbose_name='Номер серии', unique=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    count = models.IntegerField(verbose_name='Остаток', blank=False)
    product = models.ForeignKey(Product, related_name='product', verbose_name='Товар', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)


class Order(models.Model):
    date = models.DateTimeField(verbose_name='Дата заказа', auto_created=True, blank=False)
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='orders', on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name='Сумма заказа', max_digits=10, decimal_places=2)

    def __str__(self):
        return f' Заказ от {self.date} пользователь {self.user}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', verbose_name='Заказ', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='products', verbose_name='Товар', on_delete=models.CASCADE)
    series = models.ForeignKey(ProductSeries, related_name='product_series', verbose_name='Серия', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Кол-во', blank=False)
    price = models.DecimalField(verbose_name='Цена', blank=False, max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.order} {self.product} {self.price}'
