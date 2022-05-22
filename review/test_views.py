""" This module tests the review app views """

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from products.models import Type, Product
from .models import Reviews


# pylint: disable=no-member
class TestViews(TestCase):
    """
    Contains the tests for the Review app views.
    Located in views.py.
    """

    def setUp(self):
        """
        Creates a two test users, initiates the Product
        database and creates two reviews for use in testing.
        """
        john = User.objects.create_user(
            username='johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@email.com',
            password='password',
        )

        jane = User.objects.create_user(
            username='janedoe',
            first_name='Jane',
            last_name='Doe',
            email='janedoe@email.com',
            password='password',
        )

        chewy = Type.objects.create(
            name='chewy_sweets',
            friendly_name='Chewy Sweets',
        )

        bon_bons = Product.objects.create(
            type=chewy,
            name='Raspberry Bon Bons',
            description='A Chewy Sweet',
            popular_in_80s=False,
            popular_in_90s=True,
            popular_in_00s=True,
            weight_in_grams=200,
            price=Decimal(1.99),
        )

        Reviews.objects.create(
            user=john,
            product=bon_bons,
            rating=5,
            review='A nice review.',
        )

        Reviews.objects.create(
            user=jane,
            product=bon_bons,
            rating=1,
            review='A bad review.',
        )

    def test_my_reviews_view_collects_correct_objects(self):
        """
        A test to ensure the my_reviews view only renders the reviews
        of the user who made the request in the template.

        Collects all the objects in the Reviews database, asserting the total
        length is 2, this is for use in making comparisons later.

        Then signs into the 'johndoe' user created in the setUp method, before
        collecting the response of the get 'my_reviews' view. Uses Django's
        inbuilt HTTP client to ensure a status code 200 is returned and the
        template used is the correct one.

        The 'reviews' key is then collected from the context and asserted to
        having a length of 1 and the str value being that of the specified
        users review. Meaning the view has filtered the Reviews database right.
        """
        reviews = Reviews.objects.all()
        self.assertEqual(len(reviews), 2)

        self.client.login(
            email="johndoe@email.com",
            password='password',
        )

        response = self.client.get(reverse('my_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ('reviews/my_reviews.html'))

        reviews = response.context['reviews']
        self.assertEqual(len(reviews), 1)
        self.assertEqual(str(reviews[0]), 'Raspberry Bon Bons rated 5 stars')
