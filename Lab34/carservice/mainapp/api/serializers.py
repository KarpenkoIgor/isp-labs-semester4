from rest_framework import serializers

from ..models import (
    Category,
    Manufacturer,
    CarPart,
    )

class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug',
        ]


class ManufacturerSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    country = serializers.CharField(required=True)

    class Meta:
        model = Manufacturer
        fields = [
            'id', 'name', 'country',
        ]


class CarpartSerialiser(serializers.ModelSerializer):

    manufacturer = serializers.PrimaryKeyRelatedField(queryset=Manufacturer.objects)
    title = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects)
    slug = serializers.SlugField(required=True)
    image = serializers.ImageField(required=True)
    price = serializers.DecimalField(max_digits=9, decimal_places=2,required=True)

    class Meta:
        model = CarPart
        fields = '__all__'



