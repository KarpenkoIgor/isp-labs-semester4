from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Manufacturer)
admin.site.register(CarPart)
admin.site.register(PartCategory)