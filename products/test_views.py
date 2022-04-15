""" This module tests the product app views """

from django.test import TestCase
from .models import Type, Product


class TestModel(TestCase):
    """
    Contains the tests for the views.
    Located in the profile app in views.py.
    """

    def setUp(self):
        """
        Creates a Product test case.
        """
        # pylint: disable=no-member
        sour = Type.objects.create(
            name='sour_sweets',
            friendly_name='Sour Sweets',
        )

        # pylint: disable=no-member
        toxic_waste = Product.objects.create(
            type=sour,
            name='Toxic Waste',
            description='A Sour Sweet',
            year=1,
            weight_in_grams='42',
            price='4.99',
        )

    def test_get_products_page(self):
        """
        Tests the profile page renders.

        Uses the login helper method to sign into the test case User.
        Passing the views authentication conditions.
        Uses Django's in-built HTTP client to get the profile page URL.
        Asserts equal to status code 200, a successful HTTP response.
        """
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
