""" This module tests the checkout app models """

from decimal import Decimal
from django.test import TestCase
from products.models import Type, Product
from .models import Order, OrderLineItem


class TestModel(TestCase):
    """
    Contains the tests for the Order and OrderLineItem models.
    Located in the checkout app in models.py.
    """

    def setUp(self):
        """
        Initiates the Product database with an object to pass
        to the OrderLineItem model.
        Creates three Order instances for use in testing.
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

        test_order1 = Order.objects.create(
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
            order=test_order1,
            product=Product.objects.get(id=1),
            quantity=1,
        )

        test_order2 = Order.objects.create(
            order_number='Test String',
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
            order=test_order2,
            product=Product.objects.get(id=1),
            quantity=5,
        )

        test_order3 = Order.objects.create(
            order_number='Test String',
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
            order=test_order3,
            product=Product.objects.get(id=1),
            quantity=26,
        )

    def test_order_string_method_returns_order_number(self):
        """
        Tests the string method return on the Order model.

        Collects the first Order object created in the setUp method
        via its ID, storing it in the order1 variable.
        Then asserts the len of the order_number field on this variable is
        equal to 32, as is supposed to be returned from the
        generate_order_number model method.
        Then asserts the str method return on this variable is
        equal to it's order_number.

        Then collects the second Order object created in the setUp method
        via its ID, storing it in the order2 variable.
        Then asserts the str method return on this variable is
        equal to the specific string set for the order_number that
        was generated from within the setUp method.
        """

        order1 = Order.objects.get(id=1)
        self.assertEqual(len(order1.order_number), 32)
        self.assertEqual(str(order1), order1.order_number)

        order2 = Order.objects.get(id=2)
        self.assertEqual(str(order2), 'Test String')

    def test_update_total_populates_fields(self):
        """
        Tests the update_total method updates the Order model
        fields as intended.

        Collects the first Order object created in the setUp method
        via its ID, storing it in the order1 variable.
        Then asserts the values for order_total, order_weight,
        delivery_cost and grand_total are the correct values
        based of the values given to the object created within
        the Product database.

        Collects the second Order object created in the setUp method
        via its ID, storing it in the order2 variable.
        Then asserts the value for the order_weight is 1000, before
        asserting the delivery_total is 3.49, the correct value based
        of that orders weight.

        Collects the third Order object created in the setUp method
        via its ID, storing it in the order3 variable.
        Then asserts the value for the order_total is 51.74, before
        asserting the delivery_total is 0, the correct value based
        of that orders total.
        """

        order1 = Order.objects.get(id=1)
        self.assertEqual((order1.order_total), Decimal('1.99'))
        self.assertEqual((order1.order_weight), 200)
        self.assertEqual((order1.delivery_cost), Decimal('2.49'))
        self.assertEqual((order1.grand_total), Decimal('4.48'))

        order2 = Order.objects.get(id=2)
        self.assertEqual((order2.order_weight), 1000)
        self.assertEqual((order2.delivery_cost), Decimal('3.49'))

        order3 = Order.objects.get(id=3)
        self.assertEqual((order3.order_total), Decimal('51.74'))
        self.assertEqual((order3.delivery_cost), Decimal('0'))

    def test_orderlineitem_str_method_returns_product_and_order_number(self):
        """
        Tests the string method return on the OrderLine Item model.

        Collects the second OrderLineItem object created in the setUp method
        via its ID, storing it in the line_item variable.
        Then asserts the str method return on this variable is
        equal to the name of the product and the order's order_number.
        """

        line_item = OrderLineItem.objects.get(id=2)
        self.assertEqual(
            str(line_item), 'Raspberry Bon Bons on order Test String'
        )
