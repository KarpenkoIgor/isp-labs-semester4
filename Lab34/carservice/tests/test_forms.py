from django.contrib.auth.models import User
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
        "first_name": "Igor", "last_name": "Karp", "phone": "+375333330890", "buying_type": "Самовывоз", "order_date": "12/09/21",
        "comment": "Ok"
        }
    
@pytest.fixture
def incorrect_order_data():
    return {
        "first_name": "Igor", "last_name": "Karp", "phone": "+375333330890", "buying_type": "Самовывоз", "order_date": "12/09/20"
    }

@pytest.fixture
def incorrect_title_review_data():
    return {"title": "title-123", "text": "some text"}

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
