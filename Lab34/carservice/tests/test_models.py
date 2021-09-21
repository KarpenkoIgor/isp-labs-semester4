import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal

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
def carpart(image, manufacturer, category):
    return CarPart.objects.create(
        manufacturer=manufacturer, title="Part228", code="123", category=category,
        slug="test-slug", image=image, price="10.00"
        )

@pytest.fixture
def cart(customer, carpart):
    return Cart.objects.create(owner=customer, total_cost=1)

@pytest.fixture
def cart_product(customer, carpart, cart):
    return CartProduct.objects.create(user=customer,cart=cart, carpart=carpart, total_cost=Decimal(10.00))



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
def test_carpart(carpart, category):
    assert CarPart.objects.count() == 1
    assert CarPart.objects.first() == carpart 
    assert CarPart.objects.first().title == 'Part228' 
    assert CarPart.objects.first().slug == 'test-slug'
    assert CarPart.objects.first().price == Decimal(10.00)
    assert CarPart.objects.first().category == Category.objects.first()

@pytest.mark.django_db
def test_customer(customer, user):
    assert Customer.objects.count() == 1
    assert Customer.objects.first() == customer 
    assert Customer.objects.first().user == user 
    assert Customer.objects.first().phone == None
    assert Customer.objects.first().user.email == customer.user.email
    assert Customer.objects.first().phone == None
    
@pytest.mark.django_db
def test_cart_product(cart_product, customer, cart):
    assert CartProduct.objects.count() == 1
    assert CartProduct.objects.first() == cart_product
    assert CartProduct.objects.first().cart == cart

@pytest.mark.django_db
def test_cart(cart_product, customer, carpart, cart):
    assert Cart.objects.count() == 1
    assert carpart == cart_product.carpart
    assert Cart.objects.first() == cart

