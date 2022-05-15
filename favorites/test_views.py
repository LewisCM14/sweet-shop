""" This module tests the favorites app views """

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from products.models import Type, Product
from .models import Favorites


# pylint: disable=no-member
class TestViews(TestCase):
    """
    Contains the tests for the views located in the favorites app in views.py.
    """

    def setUp(self):
        """
        Creates a User test case before
        initiating the Product database with an object for testing.
        """
        User.objects.create_user(
            username='Test User',
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

    def login(self):
        """
        Helper Method

        Logs into the User created in the setUp method.
        Called in the below tests to pass user authentication conditions.
        """
        self.client.login(
            email="johndoe@email.com",
            password='password',
        )

    def test_favorite_products_post_to_the_database(self):
        """
        A view to test a user can add products to their favorites.

        Uses the login helper method to pass user authentication,
        before collecting the user instance and product object
        made in the setUp method.

        Filters the Favorites database by this user and asserts
        the length of the result is 0. Then passes the product and
        user to the reverse of the favorite url. The Favorites
        database is then filtered via the user again, asserting now
        the length of the result is 1 and the string value of the
        first index is 'Raspberry Bon Bons', the product that was passed.
        """
        self.login()

        user = User.objects.get(id=1)
        product = Product.objects.get(id=1)

        favorites = Favorites.objects.filter(user=user)
        self.assertEqual(len(favorites), 0)

        self.client.get(
            reverse("favorite", args=[product.id]), {
                'product': product,
                'user': user,
            })

        favorites = Favorites.objects.filter(user=user)
        self.assertEqual(len(favorites), 1)
        self.assertEqual(str(favorites[0]), 'Raspberry Bon Bons')

    def test_check_favorite_view_redirects_to_product(self):
        """
        A view to test when a user favorites a product they are
        redirected back to that product.

        Uses the login helper method to pass user authentication,
        before collecting the user instance and product object
        made in the setUp method.

        Then passes the product and user to the reverse of the favorite url.
        Stored in the response variable. Then uses Django's inbuilt
        HTTP client to assert a 302 redirect code is returned and the
        reverse URL for this redirect is the prodcut_detail URL
        with the id value of the product passed to the favorute URL.
        """
        self.login()

        user = User.objects.get(id=1)
        product = Product.objects.get(id=1)

        response = self.client.get(
            reverse("favorite", args=[product.id]), {
                'product': product,
                'user': user,
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("product_detail", args=[product.id]))  # noqa: E501
