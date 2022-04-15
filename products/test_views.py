""" This module tests the product app views """

from django.test import TestCase
from .models import Type, Product


class TestModel(TestCase):
    """
    Contains the tests for the views.
    Located in the product app in views.py.
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
        Product.objects.create(
            type=sour,
            name='Toxic Waste',
            description='A Sour Sweet',
            year=1,
            weight_in_grams='42',
            price='4.99',
        )

    def test_get_products_page(self):
        """
        Tests the product page renders.

        Uses Django's in-built HTTP client to get the product page URL.
        Asserts equal to status code 200, a successful HTTP response.
        """
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_get_product_detail_page(self):
        """
        Tests the product details page renders.

        Collects the Product object created in the setUp method,
        storing it in the product variable.
        Asserts it is the object created in the method via it's
        name = Toxic Waste.

        Then Uses Django's in-built HTTP client to get the product_detail URL.
        Which is an ID value of 1, as it is the only object in the database.
        Asserts equal to status code 200, a successful HTTP response.
        """
        # pylint: disable=no-member
        product = Product.objects.get(id=1)
        self.assertEqual(product.name, 'Toxic Waste')

        response = self.client.get('/products/1/')
        self.assertEqual(response.status_code, 200)
