from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Manufacturer(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название компании роизводителя')
    country = models.CharField(max_length=150, verbose_name='Страна компании роизводителя')

    def __str__(self):
        return self.name


class CategoryManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()
    
    def get_categories_for_left_sidebar(self):
        qs = list(self.get_queryset())
        data = [
            dict(
                name=category.name, url=category.get_absolute_url(), count=CarPart.objects.filter(category=category).count()
            )
            for category in qs
        ]
        return data


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Тип детали')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class CarPart(models.Model):

    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='Название детали')
    code = models.CharField(max_length=150, verbose_name='Код детали')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower() 

    def get_absolute_url(self):
        return reverse('carpart_detail', kwargs={'slug': self.slug})


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Карзина', on_delete=models.CASCADE, related_name='related_products')
    carpart = models.ForeignKey(CarPart, verbose_name='Деталь', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая стоимость')

    def __str__(self):
        return 'Деталь: {} (в корзину)'.format(self.carpart.title)

    def save(self, *args, **kwargs):
        self.total_cost = self.qty * self.carpart.price
        super().save(*args, **kwargs)



class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая стоимость')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=50, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')

    def __str__(self):
        return 'Покупатель: {} {}'.format(self.user.first_name, self.user.last_name)


class Order(models.Model):
    
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Карзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)


