""" This module tests the favorite app models """

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Type, Product
from .models import Favorites


class TestModel(TestCase):
    """
    Contains the tests for the Favorite model.
    Located in the favorite app in models.py.
    """

    def setUp(self):
        """
        Creates a test user. Then Initiates the Product database
        with an object to pass to the Favorites model.
        """

        User.objects.create_user(
            username='johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@email.com',
            password='password',
        )

        chewy = Type.objects.create(
            name='chewy_sweets',
            friendly_name='Chewy Sweets',
        )

        Product.objects.create(
            type=chewy,
            name='Raspberry Bon Bons',
            description='A Chewy Sweet',
            popular_in_80s=False,
            popular_in_90s=True,
            popular_in_00s=True,
            weight_in_grams=200,
            price=Decimal(1.99),
        )

    def test_favorites_string_method_returns_product_name(self):
        """
        Tests the string method on the Favorites model.

        Collects the User and product instance created in the setUp method.
        Then asserts the name value of the product is 'Raspberry Bon Bons'.
        Then uses these two variables to create an object in the
        Favorites database, before asserting the str value of this
        object is the products name.
        """

        user = User.objects.get(id=1)
        product = Product.objects.get(id=1)

        self.assertEqual(product.name, 'Raspberry Bon Bons')

        favorite = Favorites.objects.create(
            product=product,
            user=user,
        )

        self.assertEqual(str(favorite), 'Raspberry Bon Bons')
