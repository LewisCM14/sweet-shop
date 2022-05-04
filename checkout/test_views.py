""" This module tests the checkout app views """

from django.test import TestCase
from django.contrib.messages import get_messages


# pylint: disable=no-member
class TestProductViews(TestCase):
    """
    Contains the tests for the views located in the checkout app in views.py.
    """

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
