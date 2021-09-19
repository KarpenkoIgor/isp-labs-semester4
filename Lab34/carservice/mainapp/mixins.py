from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from .models import (
    CarPart,
    Customer,
    Cart,
    Category,
    )


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)


class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Category):
            category = Category.objects.get(slug=self.get_object().slug)
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.get_categories_for_left_sidebar()
            context['category_products'] = CarPart.objects.filter(category=category)
            return context
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.get_categories_for_left_sidebar()
        return context