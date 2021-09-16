from django.shortcuts import render
from django.views.generic import DetailView, View

from .models import (
    Filter,
    Breaks,
    Ignition,
    Suspension,
    ExhaustSystem,
    FuelSystem,
    Category,
    LatestCarparts
    )
from .mixins import CategoryDetailMixin

class BaseView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        carparts = LatestCarparts.objects.get_carparts_for_main_page(
            'filter','breaks', 'ignition', 'suspension', 'exhaustsystem', 'fuelsystem',
            with_respect_to='filter'
            )
        context ={
            'categories': categories,
            'carparts': carparts,
        }
        return render(request, 'base.html', context)


class CarpartDetailView(CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'filter': Filter,
        'breaks': Breaks,
        'ignition': Ignition,
        'suspension': Suspension,
        'exhaustsystem': ExhaustSystem,
        'fuelsystem': FuelSystem,        
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'carpart'
    template_name = 'carpart_detail.html'
    slug_url_kwarg = 'slug'


class CategoryDetailView(CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'