from django import forms
from django.contrib import admin

# Register your models here.
from .models import *



admin.site.register(Manufacturer)
admin.site.register(Category)
admin.site.register(CarPart)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)