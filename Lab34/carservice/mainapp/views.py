from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic import DetailView, View
from django.contrib.contenttypes.models import ContentType
import logging
import configparser
from threading import Thread

from .models import (
    CarPart,
    Category,
    Customer,
    Cart,
    CartProduct,
    Order,
    )
from .mixins import CartMixin, CategoryDetailMixin
from .forms import OrderForm, LoginForm, RegistrationForm
from .utils import recalc_cart


config = configparser.ConfigParser()
config.read('cnf.ini')
logging.basicConfig(
    level=config['LOGGING']['level'],
    filename=config['LOGGING']['filename']
)
log = logging.getLogger(__name__)


class BaseView(CartMixin, View):
    
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        carparts = CarPart.objects.all().order_by('-id')[:6]
        context ={
            'categories': categories,
            'carparts': carparts,
            'cart': self.cart
        }
        return render(request, 'base.html', context)


class CarpartDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = CarPart
    queryset = CarPart.objects.all()
    context_object_name = 'carpart'
    template_name = 'carpart_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if self.cart.for_anonymous_user:
            messages.add_message(request, messages.INFO, 'Для того, чтобы начать покупки необходимо авторизироваться!')
            return HttpResponseRedirect('/')
        carpart_slug = kwargs.get('slug')
        carpart = CarPart.objects.get(slug=carpart_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, carpart=carpart
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен")

        p = Thread(target=log.info, args=("{} product added".format(carpart.title),))
        p.start()
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        carpart_slug = kwargs.get('slug')
        carpart = CarPart.objects.get(slug=carpart_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, carpart=carpart,
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        p = Thread(target=log.info, args=("{} product deleted".format(carpart.title),))
        p.start()
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):
    
    def post(self, request, *args, **kwargs):
        carpart_slug = kwargs.get('slug')
        carpart = CarPart.objects.get(slug=carpart_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, carpart=carpart,
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Количество товара успешно изменено")
        p = Thread(target=log.info, args=("{} quantity changed".format(carpart.title),))
        p.start()
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories,
        }
        return render(request, 'cart.html', context)

class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart

            new_order.save()
            customer.orders.add(new_order)
            p = Thread(target=log.info, args=("{} user made order".format(form.cleaned_data['first_name'])))
            p.start()
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                username=username, password=password
            )
            if user:
                p = Thread(target=log.info, args=("User loged in"))
                p.start()
                login(request, user)
                return HttpResponseRedirect('/')
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'form': form,
            'cart': self.cart,
            'categories': categories
        }
        p = Thread(target=log.info, args=("User can't login"))
        p.start()
        return render(request, 'login.html', context)


class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            user = authenticate(
                username=new_user.username, password=form.cleaned_data['password']
            )
            login(request, user)
            p = Thread(target=log.info, args=("User registered in"))
            p.start()
            return HttpResponseRedirect('/')
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        p = Thread(target=log.info, args=("User can't register"))
        p.start()
        return render(request, 'registration.html', context)


class ProfileView(CartMixin, View):

    def get(self,request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        categories = Category.objects.get_categories_for_left_sidebar()
        p = Thread(target=log.info, args=("User loged in"))
        p.start()
        return render(
            request,
            'profile.html',
            {'orders': orders, 'cart': self.cart, 'categories': categories}
        )
