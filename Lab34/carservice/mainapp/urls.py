from django.urls import path
from .views import (
    BaseView,
    CarpartDetailView,
    CategoryDetailView,
    CartView,
    AddToCartView,
)

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('carparts/<str:ct_model>/<str:slug>', CarpartDetailView.as_view(), name='carpart_detail'),
    path('category/<str:slug>', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>', AddToCartView.as_view(), name='add_to_cart'),
]

