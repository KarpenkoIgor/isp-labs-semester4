from django.urls import path

from .api_views import (
    CategoryListAPIView,
    ManufacturerListAPIView,
    CarpartListAPIView,
    CarpartDetailAPIView,
    )


urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('manufacturers/', ManufacturerListAPIView.as_view(), name='manufacturers'),
    path('carparts/', CarpartListAPIView.as_view(), name='carparts_list'),
    path('carparts/<str:id>', CarpartDetailAPIView.as_view(), name='carpart_detail'),
]