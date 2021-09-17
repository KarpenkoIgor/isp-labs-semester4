from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View
from django.contrib.contenttypes.models import ContentType

from .models import (
    Filter,
    Breaks, 
    Ignition,
    Suspension,
    ExhaustSystem,
    FuelSystem,
    Category,
    LatestCarparts,
    Customer,
    Cart,
    CartProduct,
    )
from .mixins import CategoryDetailMixin

class BaseView(View):
    
    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_left_sidebar()
        carparts = LatestCarparts.objects.get_carparts_for_main_page(
            'filter','breaks', 'ignition', 'suspension', 'exhaustsystem', 'fuelsystem',
            with_respect_to='filter'
            )
        context ={
            'categories': categories,
            'carparts': carparts,
            'cart': cart
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context


class CategoryDetailView(CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

class AddToCartView(View):

    def get(self, request, *args, **kwargs):
        ct_model, carpart_slug = kwargs.get('ct_model'), kwargs.get('slug')
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer, in_order=False)
        content_type = ContentType.objects.get(model=ct_model)
        carpart = content_type.model_class().objects.get(slug=carpart_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=cart.owner, cart=cart, content_type=content_type, object_id=carpart.id,
        )
        if created:
            cart.products.add(cart_product)
        return HttpResponseRedirect('/cart/')

class CartView(View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': cart,
            'categories': categories,
        }
        return render(request, 'cart.html', context)
