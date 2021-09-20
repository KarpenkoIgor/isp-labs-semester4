from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from .views import recalc_cart

from .models import (
    Category,
    Manufacturer,
    CarPart,
    Customer,
    Cart,
    CartProduct,
)

User = get_user_model()

class CarserviceTestCases(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='password')
        self.category = Category.objects.create(name='Шины', slug='tyres')
        self.manufacturer = Manufacturer.objects.create(name='Ferrari', country='Италия')
        image = SimpleUploadedFile("tyre1_image.png", content=b'', content_type="image/png")
        self.carpart = CarPart.objects.create(
            category=self.category,
            title='Pirreli H80',
            manufacturer=self.manufacturer,
            slug='pirreli-h80',
            code='jk245kjh23',
            image=image,
            price=Decimal('1225.00'),
        )
        self.customer = Customer.objects.create(user=self.user, phone="375331233212", address="City")
        self.cart = Cart.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(
            user=self.customer,
            cart=self.cart,
            product=self.carpart
        )

    def test_add_to_cart(self):
        self.cart.products.add(self.cart_product)
        recalc_cart(self.cart)
        self.assertIn(self.cart_product, self.cart.products.all())
        self.assertEqual(self.cart.products.count(), 1)
        self.assertEqual(self.cart.total_cost, Decimal('1225.00'))