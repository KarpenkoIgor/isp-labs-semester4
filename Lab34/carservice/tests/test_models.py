import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from mainapp.models import (
    Manufacturer,
    CarPart,
    Category,
    Customer,
    Cart,
    CartProduct,
    Order,
)


@pytest.fixture
def user():
    return User.objects.create_user(username="test", password="123qwe456rty")

@pytest.fixture
def customer(user):
    return Customer.objects.create(user=user)

@pytest.fixture
def manufacturer():
    return Manufacturer.objects.create(name="Testwagen", country = "Тестиопа")

@pytest.fixture
def category():
    return Category.objects.create(name="filters", slug = "test-categ-slug")

@pytest.fixture
def image():
    return SimpleUploadedFile("tyre1_image.png", content=b'', content_type="image/png")

@pytest.fixture
def carpart(image, manufacturern, category):
    return CarPart.objects.create(
        manufacturer=manufacturer, title="Part228", code="123", category=category,
        slug="test-slug", image=image, price="10.00"
        )


@pytest.mark.django_db
def test_manufacturer(manufacturer):
    assert Manufacturer.objects.count() == 1
    assert Manufacturer.objects.first() == manufacturer 
    assert Manufacturer.objects.first().name == 'Testwagen' 
    assert Manufacturer.objects.first().country == 'Тестиопа'

@pytest.mark.django_db
def test_category(category):
    assert Category.objects.count() == 1
    assert Category.objects.first() == category 
    assert Category.objects.first().name == 'filters' 
    assert Category.objects.first().slug == 'test-categ-slug'

@pytest.mark.django_db
def test_carpart(carpart):
    assert CarPart.objects.count() == 1
    assert CarPart.objects.first() == carpart 
    assert CarPart.objects.first().name == 'Part228' 
    assert CarPart.objects.first().slug == 'test-slug'

