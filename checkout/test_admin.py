""" This module tests the checkout admin """

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from products.models import Type, Product
from .models import Order
from .admin import OrderAdmin


class TestAdmin(TestCase):
    """
    Contains the tests for the admin logic,
    located in the checkout app in admin.py.
    """

    def setUp(self):
        """
        Creates a User test case before
        initiating the Product database with an object.
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
        Helper Method

        Initiates an instance of the cart object within the session.
        """

        product = Product.objects.get(id=1)

        self.client.post(reverse("add_to_cart", args=[product.id]), {
            'quantity': 1,
            'redirect_url': '/products/1/',
        })

    def place_order(self):
        """
        Helper Method.

        Calls the initiate_cart method before
        creating an Order instance within the database.
        """
        self.initiate_cart()
        self.client.post(
            reverse("checkout"), {
                'full_name': 'John Doe',
                'email': 'johndoe@email.com',
                'phone_number': '11111111111',
                'street_address1': '4 privet drive',
                'street_address2': '',
                'town_or_city': 'little whinging',
                'county': 'surrey',
                'postcode': 'CR2 5ER',
                'country': 'GB',
                'client_secret': 'client secret test string',
            })

        order = Order.objects.get(id=1)
        self.client.post(
            reverse("checkout_success", args=[order.order_number])
        )

    def test_status_tuple_values_correct(self):
        """
        A test to ensure the STATUS tuple values correspond to the correct
        status value.

        Asserts the Order model STATUS tuple has the correct integer
        and string value for each index.
        """
        self.assertEqual(Order.STATUS[1], (1, 'packaged'))
        self.assertEqual(Order.STATUS[2], (2, 'posted'))
        self.assertEqual(Order.STATUS[0], (0, 'processing'))

    def test_post_order_updates_status_field(self):
        """
        A test to ensure the post_order method updates an orders status.

        Calls the place_order helper method to ensure there is an order for
        testing. Collects this order and asserts the status field has
        defaulted to processing. Then calls the post_order method from within
        the OrderAdmin on it before then asserting the status field has been
        updated to the 2, or 'posted'.
        """
        self.place_order()

        order = Order.objects.get(id=1)
        self.assertEqual(order.status, 0)

        OrderAdmin.post_order(self, 'POST', [order])
        self.assertEqual(order.status, 2)

    def test_package_order_updates_status_field(self):
        """
        A test to ensure the package_order method updates an orders status.

        Calls the place_order helper method to ensure there is an order for
        testing. Collects this order and asserts the status field has
        defaulted to processing. Then calls the package_order method
        from within the OrderAdmin on it before then asserting the
        status field has been updated to the 1, or 'packaged'.
        """
        self.place_order()

        order = Order.objects.get(id=1)
        self.assertEqual(order.status, 0)

        OrderAdmin.package_order(self, 'POST', [order])
        self.assertEqual(order.status, 1)

    def test_process_order_updates_status_field(self):
        """
        A test to ensure the process_order method updates an orders status.

        Calls the place_order helper method to ensure there is an order for
        testing. Collects this order and asserts the status field has
        defaulted to processing. Then calls the package_order method
        from within the OrderAdmin on it before then asserting the
        status field has been updated to the 1, or 'packaged'.

        Then calls the process_order method from within the OrderAdmin
        on the order, before then asserting the status field has been
        updated to the 0, or 'processing'.
        """
        self.place_order()

        order = Order.objects.get(id=1)
        self.assertEqual(order.status, 0)

        OrderAdmin.package_order(self, 'POST', [order])
        self.assertEqual(order.status, 1)

        OrderAdmin.process_order(self, 'POST', [order])
        self.assertEqual(order.status, 0)
