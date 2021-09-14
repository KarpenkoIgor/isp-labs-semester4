from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()

def get_carpart_url(obj, viewname, model_name):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})

class Manufacturer(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название компании роизводителя')
    country = models.CharField(max_length=150, verbose_name='Страна компании роизводителя')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Тип детали')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class CarPart(models.Model):
    class Meta:
        abstract = True

    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='Название детали')
    code = models.CharField(max_length=150, verbose_name='Код детали')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title




#------Groups of CarParts------------------------------
class Filter(CarPart):
    filter_design = models.CharField(max_length=255, verbose_name = 'Исполнение фильтра')
    length = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Длинна(в мм)')
    height = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Высота(в мм)')
    width = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Ширина(в мм)')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_carpart_url(self, 'carpart_detail')

class Breaks(CarPart):
    instalation_side = models.CharField(max_length=255, verbose_name='Сторона утановки')
    disk_type = models.CharField(max_length=255, verbose_name='Тип диска')
    length = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Длинна(в мм)')
    thickness = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Толщина(в мм)')
    holes_number = models.PositiveIntegerField(default=0, verbose_name='Количество отвестий')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_carpart_url(self, 'carpart_detail')


class Ignition(CarPart):
    material = models.CharField(max_length=255, verbose_name='Матриал')
    ignition_wire = models.CharField(max_length=255, verbose_name='Провод зажигания')
    ignition_coil = models.CharField(max_length=255, verbose_name='Катушка зажигания')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_carpart_url(self, 'carpart_detail')

class Suspension(CarPart):
    instalation_side = models.CharField(max_length=255, verbose_name='Сторона утановки')
    system = models.CharField(max_length=255, verbose_name='Система амортизатора')
    mounting_method = models.CharField(max_length=255, verbose_name='Споспоб крепления')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_carpart_url(self, 'carpart_detail')

class ExhaustSystem(CarPart):
    weight = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Вес(в мм)')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

class FuelSystem(CarPart):
    pressure = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Давление(в Бар)')
    color = models.CharField(max_length=255, verbose_name='Цвет')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_carpart_url(self, 'carpart_detail')

#------------------------------------------------------

class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Карзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
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
