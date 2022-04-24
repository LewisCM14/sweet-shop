""" This module tests the cart app views """

from django.test import TestCase
from products.models import Type, Product


# pylint: disable=no-member
class TestView(TestCase):
    """
    Contains the tests for the views located in the cart app in views.py.
    """
    def setUp(self):
        """
        Creates a Product database test case.
        """
        sour = Type.objects.create(
            name='sour',
            friendly_name='Sour',
        )

        chewy = Type.objects.create(
            name='chewy',
            friendly_name='Chewy'
        )

        Product.objects.create(
            type=sour,
            name='Toxic Waste',
            description='A sour Sweet',
            popular_in_80s=True,
            popular_in_90s=True,
            popular_in_00s=True,
            weight_in_grams='42',
            price='4.99',
        )

        Product.objects.create(
            type=chewy,
            name='Bon Bons',
            description='A chewy Sweet',
            popular_in_80s=False,
            popular_in_90s=False,
            popular_in_00s=True,
            weight_in_grams='75',
            price='2.99',
        )

    def test_get_cart_page(self):
        """
        Tests the view_cart page renders.

        Uses Django's in-built HTTP client to get the product page URL.
        Asserts equal to status code 200, a successful HTTP response.
        """

        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
