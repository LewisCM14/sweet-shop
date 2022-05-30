""" This module tests the products app models """

from django.test import TestCase
from .models import Type, Product


class TestModel(TestCase):
    """
    Contains the tests for the Type & Product models.
    Located in the products app in models.py.
    """

    def test_type_string_method_returns_name(self):
        """
        Tests the string method on the Type model.

        Creates a Type instance. Then fetches the object created
        in the Type database for this instance via id,
        storing this in the sour variable.
        Then asserts the string method, returned on this variable,
        returns the name value of the instance, which is sour_sweets.
        """

        Type.objects.create(
            name='sour_sweets',
            friendly_name='Sour Sweets',
        )

        sour = Type.objects.get(id=1)
        self.assertEqual(str(sour), 'sour_sweets')

    def test_get_friendly_name_returns_friendly_name(self):
        """
        Tests the get_friendly_name method on the Type model.

        Creates a Type instance. Then fetches the object created
        in the Type database for this instance via id,
        storing this in the sour variable.
        Then asserts when the method is ran on this variable,
        the result returned is the instances friendly_name value.
        In this case Sour Sweets
        """
        Type.objects.create(
            name='sour_sweets',
            friendly_name='Sour Sweets',
        )

        sour = Type.objects.get(id=1)
        self.assertEqual(Type.get_friendly_name(sour), 'Sour Sweets')

    def test_product_string_method_returns_name(self):
        """
        Tests the string method on the Product model.

        Creates a Type instance,
        then creates a Product instance with this type.
        Then fetches the object created in the Product database,
        for this instance via id, storing this in the toxic variable.
        Then asserts the string method, returned on this variable,
        returns the name value of the instance, which is Toxic Waste.
        """

        sour = Type.objects.create(
            name='sour_sweets',
            friendly_name='Sour Sweets',
        )

        Product.objects.create(
            type=sour,
            name='Toxic Waste',
            description='A Sour Sweet',
            popular_in_80s=False,
            popular_in_90s=True,
            popular_in_00s=True,
            weight_in_grams='42',
            price='4.99',
        )

        toxic = Product.objects.get(id=1)
        self.assertEqual(str(toxic), 'Toxic Waste')
