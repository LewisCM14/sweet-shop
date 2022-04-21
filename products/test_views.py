""" This module tests the product app views """

from django.test import TestCase
from django.contrib.messages import get_messages
from .models import Type, Product


# pylint: disable=no-member
class TestView(TestCase):
    """
    Contains the tests for the views located in the product app in views.py.
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

    def test_get_products_page(self):
        """
        Tests the product page renders.

        Collects the products created in the setUp method,
        storing it in the products variable. Asserts the length of this is 2.
        Meaning all the products can be found.

        Uses Django's in-built HTTP client to get the product page URL.
        Asserts equal to status code 200, a successful HTTP response.
        """
        products = Product.objects.all()
        self.assertEqual(len(products), 2)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_get_product_detail_page(self):
        """
        Tests the product details page renders.

        Collects the first Product object created in the setUp method,
        storing it in the product variable.
        Asserts it is the object created in the method via it's
        name = Toxic Waste.

        Then Uses Django's in-built HTTP client to get the product_detail URL.
        Which is an ID value of 1, as it is the first object in the database.
        Asserts equal to status code 200, a successful HTTP response.
        """
        product = Product.objects.get(id=1)
        self.assertEqual(product.name, 'Toxic Waste')

        response = self.client.get('/products/1/')
        self.assertEqual(response.status_code, 200)

    def test_valid_search_input_returns_objects(self):
        """
        Tests the all_products view returns objects when a q value is sent.

        Uses Django's in-built HTTP client to get the query URL.
        Ensuring when the string 'toxic' is searched
        a status code 200 is returned, a successful HTTP response.
        """
        response = self.client.get('/products/?q=toxic')
        self.assertEqual(response.status_code, 200)

    def test_blank_search_input_is_handled(self):
        """
        Tests the all_products view handles a blank input q value.

        Uses Django's in-built HTTP client to get the blank query URL.
        Ensuring the correct error message is returned in the response.
        Before then ensuring the user is redirected to the all products url.
        """
        response = self.client.get('/products/?q=')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You didn't enter any search criteria!")  # noqa

        self.assertRedirects(response, '/products/')

    def test_can_filter_products_by_type(self):
        """
        Tests the all_products view filters objects by type.

        Attempts to filter the Product database created in the setUp method
        by the 'sour' type. Storing it in the products variable.
        Asserts the length of this is 1.
        Meaning the database has been successfully filtered by the 'sour' type.

        Then Uses Django's in-built HTTP client to get the query URL.
        Ensuring when the type 'sour' is searched
        a status code 200 is returned, a successful HTTP response.
        """
        products = Product.objects.filter(type=1)
        self.assertEqual(len(products), 1)

        response = self.client.get('/products/?type_query=sour')
        self.assertEqual(response.status_code, 200)

    def test_can_filter_products_by_year(self):
        """
        Tests the all_products view filters objects by year.

        Filters the objects created in the setUp method by the
        years_popular fields, ensuring the length of the returned
        variable is correct as per the database.

        Then Uses Django's in-built HTTP client to get the query URL.
        Ensuring for each of the three years a status code 200 is returned.
        A successful HTTP response.
        """
        products = Product.objects.filter(popular_in_80s=True)
        self.assertEqual(len(products), 1)

        products = Product.objects.filter(popular_in_90s=True)
        self.assertEqual(len(products), 1)

        products = Product.objects.filter(popular_in_00s=True)
        self.assertEqual(len(products), 2)

        response = self.client.get('/products/?year=80')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/?year=90')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/?year=00')
        self.assertEqual(response.status_code, 200)

    def test_can_sort_products_by_name(self):
        """
        Tests the all_products view sorts objects by name.

        Uses Django's in-built HTTP client to get the sort URL's.
        Ensuring a status code 200 is returned. A successful HTTP response.
        """
        response = self.client.get('/products/?sort=name&direction=asc')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/?sort=name&direction=desc')
        self.assertEqual(response.status_code, 200)

    def test_can_sort_products_by_type(self):
        """
        Tests the all_products view sorts objects by type.

        Uses Django's in-built HTTP client to get the sort URL's.
        Ensuring a status code 200 is returned. A successful HTTP response.
        """
        response = self.client.get('/products/?sort=type&direction=asc')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/?sort=type&direction=desc')
        self.assertEqual(response.status_code, 200)

    def test_can_sort_products_by_price(self):
        """
        Tests the all_products view sorts objects by price.

        Uses Django's in-built HTTP client to get the sort URL's.
        Ensuring a status code 200 is returned. A successful HTTP response.
        """
        response = self.client.get('/products/?sort=price&direction=asc')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/?sort=price&direction=desc')
        self.assertEqual(response.status_code, 200)
