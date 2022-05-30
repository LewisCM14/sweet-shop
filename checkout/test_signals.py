""" This module tests the signals in checkout app """

from decimal import Decimal
from django.test import TestCase
from products.models import Type, Product
from .models import Order, OrderLineItem


class TestSignals(TestCase):
    """
    Contains the tests for the signals.
    Located in the checkout app in signals.py.
    """

    def setUp(self):
        """
        Initiates the Product database with two object to pass
        to the OrderLineItem model.
        Creates an Order instance with two line items for use in testing.
        """
        fizzy = Type.objects.create(
            name='fizzy_sweets',
            friendly_name='Fizzy Sweets',
        )

        Product.objects.create(
            type=fizzy,
            name='Fizzy Twin Cherries',
            description='A Fizzy Sweet',
            popular_in_80s=False,
            popular_in_90s=True,
            popular_in_00s=True,
            weight_in_grams=200,
            price=Decimal(1.99),
        )

        Product.objects.create(
            type=fizzy,
            name='Fizzy Bubblegum Bottles',
            description='A fizzy Sweet',
            popular_in_80s=True,
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

        OrderLineItem.objects.create(
            order=test_order,
            product=Product.objects.get(id=2),
            quantity=5,
        )

    def test_post_delete_signal_updates_totals(self):
        """
        Tests the update_total method updates the Order model
        fields as intended when a OrderLineItem is deleted.

        Collects the Order object created in the setUp method
        via its ID, storing it in the order variable.
        Then asserts the values for order_total, order_weight,
        delivery_cost and grand_total are the correct values
        based of the values given to the products created within
        the Product database.

        Then collects the second line item created in the setUp method
        and deletes it, before collecting the Order object again and
        asserting the four fields have been updated to the correct values
        after the post_delete event has been triggered.
        """

        order = Order.objects.get(id=1)
        self.assertEqual((order.order_total), Decimal('11.94'))
        self.assertEqual((order.order_weight), 1200)
        self.assertEqual((order.delivery_cost), Decimal('3.49'))
        self.assertEqual((order.grand_total), Decimal('15.43'))

        bubblegum_bottles = OrderLineItem.objects.get(id=2)
        bubblegum_bottles.delete()

        order = Order.objects.get(id=1)
        self.assertEqual((order.order_total), Decimal('1.99'))
        self.assertEqual((order.order_weight), 200)
        self.assertEqual((order.delivery_cost), Decimal('2.49'))
        self.assertEqual((order.grand_total), Decimal('4.48'))
