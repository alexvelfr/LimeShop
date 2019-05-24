from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(verbose_name='Номер телефона', blank=True, max_length=20)


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=150, unique=True, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'


class Product(models.Model):
    name = models.CharField(verbose_name='Название товара', max_length=150, unique=True, blank=False)
    category = models.ForeignKey(ProductCategory, verbose_name='Категория', related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductSeries(models.Model):
    number = models.IntegerField(verbose_name='Номер серии', unique=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    count = models.IntegerField(verbose_name='Остаток', blank=False)
    product = models.ForeignKey(Product, related_name='product_series', verbose_name='Товар', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product} №{self.number}'

    class Meta:
        verbose_name = 'Серия товара'
        verbose_name_plural = 'Серии товаров'


class Order(models.Model):
    date = models.DateTimeField(verbose_name='Дата заказа', auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='orders', on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name='Сумма заказа', max_digits=10, decimal_places=2, blank=True)

    def __str__(self):
        return f'Заказ от {self.date.strftime("%Y.%m.%d %H:%M:%S")} пользователь {self.user}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItems(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', verbose_name='Заказ', on_delete=models.CASCADE, blank=False)
    series = models.ForeignKey(ProductSeries, related_name='products_in_order', verbose_name='Серия', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Кол-во', blank=False)
    price = models.DecimalField(verbose_name='Цена', blank=True, max_digits=10, decimal_places=2)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.price = self.series.price * self.count
        super().save()
        # Спишем остаток
        self.series.count -= self.count
        self.series.save()
        # Обновим сумму в заказе
        self.order.amount = self.order.order_items.aggregate(Sum('price')).get('price__sum')
        self.order.save()

    def __str__(self):
        return f'{self.series} {self.price}грн. {self.order}'

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

