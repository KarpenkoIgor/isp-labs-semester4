from django.contrib.auth.models import User
from datetime import date
import pytest

from mainapp.forms import RegistrationForm, LoginForm, OrderForm


@pytest.fixture
def user_reg_data():
    return {"username": "test", "password": "123qwe456rty", "confirm_password": "123qwe456rty" , "email": "test@mail.com"}

@pytest.fixture
def log_data():
    return {"username": "test", "password": "123qwe456rty"}

@pytest.fixture
def incorrect_log_data():
    return {"username": "test", "password": "123qwe456rrty"}

@pytest.fixture
def order_data():
    return {
        "first_name": "Igor", "last_name": "Karp", "phone": "+375333330890", "address": "Beke", "buying_type": "Самовывоз", 
        "order_date": date(2021,12,12)," comment": "Ok"
        }
    
@pytest.fixture
def incorrect_order_data():
    return {
        "first_name": "Igor", "last_name": "Karp", "phone": "+375333330890", "buying_type": "Самовывоз", 
        "order_date": date(2020, 12, 12)
    }

@pytest.fixture
def user():
    return User.objects.create_user(username="test", password="123qwe456rty")

@pytest.mark.django_db
def test_user_reg(user_reg_data):
    assert RegistrationForm(data=user_reg_data).is_valid()

@pytest.mark.django_db
def test_user_log(user, log_data, incorrect_log_data):
    assert LoginForm(data=log_data).is_valid()
    assert not LoginForm(data=incorrect_log_data).is_valid()

@pytest.mark.django_db
def test_make_order(user, incorrect_order_data, order_data):
    assert not OrderForm(data=incorrect_order_data).is_valid()
