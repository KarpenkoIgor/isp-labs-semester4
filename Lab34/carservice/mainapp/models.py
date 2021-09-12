from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Manufacturer(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название компании роизводителя')
    country = models.CharField(max_length=150, verbose_name='Страна компании роизводителя')

    def __str__(self):
        return self.name


class PartCategory(models.Model):
    name = models.CharField(max_length=150, verbose_name='Тип детали')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class CarPart(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='Название детали')
    category = models.ForeignKey(PartCategory, verbose_name='Категория', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Карзина', on_delete=models.CASCADE, related_name='related_products')
    car_part = models.ForeignKey(CarPart, verbose_name='Деталь', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая стоимость')

    def __str__(self):
        return 'Деталь: {} (в корзину)'.format(self.car_part.title)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая стоимость')

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, verbose_name='Номер телефона')
    address = models.CharField(max_length=50, verbose_name='Адрес')

    def __str__(self):
        return 'Покупатель: {} {}'.format(self.user.first_name, self.user.last_name)
