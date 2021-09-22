from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
import pytest
from datetime import date

from mainapp.forms import RegistrationForm, LoginForm, OrderForm
from mainapp.models import (
    Manufacturer,
    CarPart,
    Category,
    Customer,
    Cart,
    CartProduct,
    Order,
)


User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(username="test", password="123qwe456rty")

@pytest.fixture
def user2():
    return User.objects.create_user(username="test2", password="123qwe456rty")

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


@pytest.mark.parametrize('param', [
    ('registration'),
    ('login'),
    ('logout'),
])

@pytest.mark.django_db
def test_render_views(client, param):
    temp_url = reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200 or resp.status_code == 302

@pytest.mark.django_db
def test_register(client):
    data = {"username": "test", "password": "123qwe456rty", "confirm_password": "123qwe456rty", 
        "email" : "mypost@mail.com", 
    }
    assert RegistrationForm(data=data).is_valid() 
    assert User.objects.count() == 0
    reg_url = reverse('registration')
    resp = client.post(reg_url, data)
    assert User.objects.count() == 1
    assert resp.status_code == 200 or resp.status_code == 302

@pytest.mark.django_db
def test_login(client, user):
    data = {"username": user.username, "password": "123qwe456rty"}
    login_url = reverse('login')
    resp = client.post(login_url, data)
    assert client.post(login_url, username=user.username, password="123qwe456rty")
    assert client.login(username=user.username, password="123qwe456rty")
    assert resp.status_code == 200 or resp.status_code == 302

 
@pytest.mark.django_db
def test_add_to_cart(client, customer, carpart, cart):
    client.login(username=customer.user.username, password="123qwe456rty")
    data = {"slug": carpart.slug , "cart": cart, "carpart": carpart} 
    add_url = reverse('add_to_cart', kwargs={'slug': carpart.slug})
    assert CartProduct.objects.count() == 0
    resp = client.get(add_url, data)
    assert resp.status_code == 200 or resp.status_code == 302
    assert CartProduct.objects.count() == 1
    assert Cart.objects.last().total_cost == Decimal(carpart.price)

@pytest.mark.django_db
def test_add_to_cart_without_log(client, customer, carpart, cart):
    data = {"slug": carpart.slug , "cart": cart, "carpart": carpart} 
    add_url = reverse('add_to_cart', kwargs={'slug': carpart.slug})
    assert CartProduct.objects.count() == 0
    resp = client.get(add_url, data)
    assert CartProduct.objects.count() == 0
    assert resp.status_code == 200 or resp.status_code == 302


@pytest.mark.django_db
def test_delete_to_cart(client, customer, user, carpart):
    client.login(username=user.username, password="123qwe456rty")
    data = {"slug": carpart.slug , "carpart": carpart}    
    delete_url = reverse('delete_from_cart', kwargs={'slug': carpart.slug})
    add_url = reverse('add_to_cart', kwargs={'slug': carpart.slug})
    assert CartProduct.objects.count() == 0
    resp = client.get(add_url, data)
    assert resp.status_code == 200 or resp.status_code == 302
    assert CartProduct.objects.count() == 1
    resp = client.get(delete_url, data)
    assert resp.status_code == 200 or resp.status_code == 302
    assert CartProduct.objects.count() == 0

@pytest.mark.django_db
def test_change_qty(client, customer, user, carpart):
    client.login(username=user.username, password="123qwe456rty")
    data = {"slug": carpart.slug , "qty": 4}     
    add_url = reverse('add_to_cart', kwargs={'slug': carpart.slug})
    url = reverse('change_qty', kwargs={'slug': carpart.slug})
    assert CartProduct.objects.count() == 0
    resp = client.get(add_url, data)
    assert resp.status_code == 200 or resp.status_code == 302
    assert CartProduct.objects.count() == 1
    assert CartProduct.objects.last().qty == 1
    resp = client.post(url, data)
    assert resp.status_code == 200 or resp.status_code == 302
    assert CartProduct.objects.last().qty == 4

@pytest.mark.django_db
def test_base_view(client, user):
        url = reverse('base')
        client.login(username=user.username, password="123qwe456rty")
        resp = client.get(url)
        assert resp.status_code == 200 or resp.status_code == 302

@pytest.mark.django_db
def test_carpart_detail_view(client, carpart, user):
        client.login(username=user.username, password="123qwe456rty")
        url = reverse('carpart_detail', kwargs={'slug': carpart.slug})
        resp = client.get(url)
        assert resp.status_code == 200 or resp.status_code == 302

@pytest.mark.django_db
def test_category_detail_view(client, category, user):
        client.login(username=user.username, password="123qwe456rty")
        url = reverse('category_detail', kwargs={'slug': category.slug})
        resp = client.get(url)
        assert resp.status_code == 200 or resp.status_code == 302
       
@pytest.mark.django_db
def test_cart_view(client, cart, user):
        client.login(username=user.username, password="123qwe456rty")
        url = reverse('cart')
        resp = client.get(url)
        assert resp.status_code == 200 or resp.status_code == 302
        
@pytest.mark.django_db
def test_checkout_view(client, cart, user):
        client.login(username=user.username, password="123qwe456rty")
        url = reverse('checkout')
        resp = client.get(url)
        assert resp.status_code == 200 or resp.status_code == 302

@pytest.mark.django_db
def test_profile_view(client, cart, user):
        client.login(username=user.username, password="123qwe456rty")
        url = reverse('profile')
        resp = client.get(url)
        assert resp.status_code == 200 or resp.status_code == 302

@pytest.mark.django_db
def test_make_order(client, customer, user, carpart):
    client.login(username=user.username, password="123qwe456rty")
    data = {"slug": carpart.slug , "qty": 4}  
    order_data = {
        "first_name": "Micha", "last_name": "Gen", "phone": "+1234", "buying_type": "Самовывоз",
        "order_date": date(2021, 12, 12),
    }   
    add_url = reverse('add_to_cart', kwargs={'slug': carpart.slug})
    url = reverse('change_qty', kwargs={'slug': carpart.slug})
    make_order_view_url = reverse('make_order')
    assert CartProduct.objects.count() == 0
    resp = client.get(add_url, data)
    assert resp.status_code == 200 or resp.status_code == 302
    assert CartProduct.objects.count() == 1
    assert CartProduct.objects.last().qty == 1
    resp = client.post(url, data)
    assert resp.status_code == 200 or resp.status_code == 302
    assert CartProduct.objects.last().qty == 4
    assert Order.objects.count() == 0
    resp = client.post(make_order_view_url, order_data)
    assert resp.status_code == 200 or resp.status_code == 302

