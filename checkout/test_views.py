""" This module tests the checkout app views """

from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from products.models import Type, Product


# pylint: disable=no-member
class TestViews(TestCase):
    """
    Contains the tests for the views located in the checkout app in views.py.
    """
    def setUp(self):
        """
        Initiates the Product database with an object for testing.
        """
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

    def initiate_cart(self):
        """
        A helper method to initiate an instance of the cart object.
        Then stored within the session, used to then prefrom tests on.

        Then collects the created session,
        storing it in the 'session' variable. From this variable
        asserts the 'cart' key has a length of 1.
        Meaing a cart object has been created and a key:value pair passed.

        From the session variable then collects the cart dict itself,
        storing it in the cart variable. From here asserts that the
        value of the key '1' is the integer 1. Meaning the product with an ID
        of '1' has a quantity of 1 stored within the cart dict.

        These tests are done as it is imperative the method creates a cart
        object within the session, and the key:value pair in it is pre-defined.
        """

        product = Product.objects.get(id=1)
        quantity = 1

        self.client.post(reverse("add_to_cart", args=[product.id]), {
            'quantity': quantity,
            'redirect_url': '/products/1/',
        })

        session = self.client.session
        self.assertEqual(len(session['cart']), 1)

        cart = session['cart']
        self.assertEqual(cart.get('1'), quantity)

    def test_checkout_page_redirects_if_cart_empty(self):
        """
        Tests the checkout page redirects to the product page if
        the cart is empty.

        Uses Django's in-built HTTP client to get the checkout page URL.
        Storing it in the response variable. Then asserts the status code
        on this is equal to a 302 redirect response.
        Then using Django's get_messages method asserts a error message
        with the desired string value is returned to the user before asserting
        the redirect URL is the products page.
        """

        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "There's nothing in your cart at the moment")  # noqa: E501
        self.assertRedirects(response, '/products/')

    def test_checkout_page_renders(self):
        """
        Tests the checkout page renders.

        Initiates a cart instance in the session with the initiate_cart
        helper method.

        Uses Django's in-built HTTP client to get the checkout page URL.
        Storing it in the response variable. Then asserts the status code
        on this is equal to a 200, a successful HTTP response.
        """

        self.initiate_cart()
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
