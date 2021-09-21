from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializers import (
    CategorySerializer, 
    ManufacturerSerializer, 
    CarpartSerialiser,
    )
from ..models import Category, Manufacturer, CarPart


class CategoryListAPIView(ListAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ManufacturerListAPIView(ListAPIView):

    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()


class CarpartListAPIView(ListAPIView):

    serializer_class = CarpartSerialiser
    queryset = CarPart.objects.all()


class CarpartDetailAPIView(RetrieveAPIView):

    serializer_class = CarpartSerialiser
    queryset = CarPart.objects.all()
    lookup_field = 'id'
