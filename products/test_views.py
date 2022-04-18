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

    def test_valid_search_input_returns_objects(self):
        """
        Tests the all_products view returns objects when a q value is sent.

        Collects the product created in the setUp method,
        storing it in the products variable. Asserts the length of this is 1.
        Sets the 'q' value as the string toxic,
        then passes it to the query variable. Ensuring it is equal to 'toxic'.

        Then Uses Django's in-built HTTP client to get the query URL.
        Ensuring when the string 'toxic' is searched
        a status code 200 is returned, a successful HTTP response.
        """
        # pylint: disable=no-member
        products = Product.objects.all()
        self.assertEqual(len(products), 1)

        # pylint: disable=invalid-name
        q = 'toxic'
        query = q
        self.assertEqual(query, 'toxic')

        response = self.client.get('/products/?q=toxic')
        self.assertEqual(response.status_code, 200)
