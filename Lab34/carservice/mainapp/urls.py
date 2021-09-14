from django.urls import path
from .views import (
    test_view,
    CarpartDetailView
)

urlpatterns = [
    path('', test_view, name='base'),
    path('carparts/<str:ct_model>/<str:slug>', CarpartDetailView.as_view(), name='carpart_detail'),
]

