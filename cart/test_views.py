""" This module tests the cart app views """

from django.test import TestCase
from django.urls import reverse
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

    def test_cart_view_renders(self):
        """
        Tests the view_cart page renders.

        Uses Django's in-built HTTP client to get the product page URL.
        Asserts equal to status code 200, a successful HTTP response.
        """

        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_redirects_to_item(self):
        """
        Tests the add_to_cart view redirects back to the product_detail
        page of the product added.

        Passes the ID for the product created in the setUp method as the
        argument to the reverse of the add_to_cart url,
        with a quantity of 1 and redirect_url value for that of the product.

        Uses Django's in-built HTTP client to asserts the status code is
        equal to 302, a successful HTTP redirect response. Before asserting the
        redirect url is the correct one for the object added.
        """

        response = self.client.post(reverse("add_to_cart", args=[1]), {
            'quantity': '1',
            'redirect_url': '/products/1/',
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products/1/')
