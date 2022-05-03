""" This module tests the checkout app models """

from decimal import Decimal
from django.test import TestCase
from products.models import Type, Product
from .models import Order, OrderLineItem


# pylint: disable=no-member
class TestModel(TestCase):
    """
    Contains the tests for the Order and OrderLineItem models.
    Located in the checkout app in models.py.
    """

    def setUp(self):
        """
        Initiates the Product database with an object to pass
        to the OrderLineItem model.
        Creates an Order instance for use in testing.
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

        test_order = Order.objects.create(
            user_profile=None,
            full_name='John Doe',
            email='johndoe@email.com',
            phone_number='11111111111',
            street_address1='4 privet drive',
            street_address2='',
            town_or_city='little whinging',
            county='surrey',
            postcode='CR2 5ER',
            country='GB',
        )

        OrderLineItem.objects.create(
            order=test_order,
            product=Product.objects.get(id=1),
            quantity=1,
        )

    def test_order_string_method_returns_order_number(self):
        """
        Tests the string method return on the Order model.

        Collects the Order object created in the setUp method
        via its ID, storing it in the order variable.
        Then asserts the str method return on this variable is
        equal to it's order_number.
        """

        order = Order.objects.get(id=1)
        self.assertEqual(str(order), order.order_number)
