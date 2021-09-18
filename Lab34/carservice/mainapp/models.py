from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.utils import timezone

User = get_user_model()

def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_carpart_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class LatestCarpartsManager:

    @staticmethod
    def get_carparts_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        carparts = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_carparts = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            carparts.extend(model_carparts)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        carparts, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return carparts


class LatestCarparts:

    objects = LatestCarpartsManager()


class Manufacturer(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название компании роизводителя')
    country = models.CharField(max_length=150, verbose_name='Страна компании роизводителя')

    def __str__(self):
        return self.name

class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Фильтры' : 'filter__count',
        'Тормозная система' : 'breaks__count',
        'Зажигание' : 'ignition__count',
        'Подвеска' : 'suspension__count',
        'Система выпуска' : 'exhaustsystem__count',
        'Топливная система' : 'fuelsystem__count',
    }
    def get_queryset(self):
        return super().get_queryset()
    
    def get_categories_for_left_sidebar(self):
        models = get_models_for_count(
            'filter', 'breaks', 'ignition', 'suspension', 'exhaustsystem', 'fuelsystem'
            )
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
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

    def get_model_name(self):
        return self.__class__.__name__.lower() 


#------Groups of CarParts------------------------------
class Filter(CarPart):
    length = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Длинна(в мм)')
    height = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Высота(в мм)')
    width = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Ширина(в мм)')
    filter_design = models.CharField(max_length=255, verbose_name = 'Исполнение фильтра')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_carpart_url(self, 'carpart_detail')


class Breaks(CarPart):
    instalation_side = models.CharField(max_length=255, verbose_name='Сторона утановки')
    disk_type = models.CharField(max_length=255, verbose_name='Тип диска')
    height = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Высота(в мм)')
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
    weight = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Вес(в граммах)')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)
    
    def get_absolute_url(self):
        return get_carpart_url(self, 'carpart_detail')


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
        return 'Деталь: {} (в корзину)'.format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.total_cost = self.qty * self.content_object.price
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

    def save(self, *args, **kwargs):
        cart_data = self.products.aggregate(models.Sum('total_cost'), models.Count('id'))
        if cart_data.get('total_cost__sum'):
            self.total_cost = cart_data['total_cost__sum']
        else:
            self.total_cost = 0
        self.total_products = cart_data['id__count']
        super().save(*args, **kwargs)


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
        return str(seld.id)


