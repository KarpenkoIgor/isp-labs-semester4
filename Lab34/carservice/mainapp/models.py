from django.db import models

# Create your models here.
#1.Carparts
#2.Cars
#3.Type of parts
#4.Car/Carparts manufacturer
#5.Detail offer
#6.Rapair offer


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
