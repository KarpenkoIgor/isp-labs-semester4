from django import forms
from django.contrib import admin

# Register your models here.
from .models import *


class FilterCategoryChoiceField(forms.ModelChoiceField):
    pass


class FilterAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return FilterCategoryChoiceField(Category.objects.filter(slug='filters'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class BreaksCategoryChoiceField(forms.ModelChoiceField):
    pass


class BreaksAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return BreaksCategoryChoiceField(Category.objects.filter(slug='breaks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class IgnitionCategoryChoiceField(forms.ModelChoiceField):
    pass


class IgnitionAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return IgnitionCategoryChoiceField(Category.objects.filter(slug='ignitions'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SuspensionCategoryChoiceField(forms.ModelChoiceField):
    pass


class SuspensionAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return SuspensionCategoryChoiceField(Category.objects.filter(slug='suspensions'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class ExhaustSystemCategoryChoiceField(forms.ModelChoiceField):
    pass


class ExhaustSystemAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ExhaustSystemCategoryChoiceField(Category.objects.filter(slug='exhaustsystems'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FuelSystemCategoryChoiceField(forms.ModelChoiceField):
    pass


class FuelSystemAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return FuelSystemCategoryChoiceField(Category.objects.filter(slug='fuelsystems'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Manufacturer)
admin.site.register(Category)
admin.site.register(Filter, FilterAdmin)
admin.site.register(Breaks, BreaksAdmin)
admin.site.register(Ignition, IgnitionAdmin)
admin.site.register(Suspension, SuspensionAdmin)
admin.site.register(ExhaustSystem, ExhaustSystemAdmin)
admin.site.register(FuelSystem, FuelSystemAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)