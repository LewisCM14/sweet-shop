""" This module tests the review app models """

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User

from products.models import Type, Product
from .models import Reviews


class TestModel(TestCase):
    """
    Contains the tests for the Reviews model.
    Located in the review app in models.py.
    """

    def setUp(self):
        """
        Creates a test user and initiated the Product
        database for use in testing.
        """
        User.objects.create_user(
            username='johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@email.com',
            password='password',
        )

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

    def test_str_method_return_of_reviews_model(self):
        """
        Tests the string method on the Reviews model.

        Fetches the User and Product objects created in the setUp method,
        before creating an Reviews instance with these.

        It is then asserted the return of the str method for this instance
        is the product name followed by the rating.
        """
        user = User.objects.get(id=1)
        product = Product.objects.get(id=1)

        review = Reviews.objects.create(
            user=user,
            product=product,
            rating=5,
            review='Some String',
        )

        self.assertEqual(
            str(review), f'{review.product.name} rated {review.rating} stars'
        )
        self.assertEqual(str(review), 'Raspberry Bon Bons rated 5 stars')
