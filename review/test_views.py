""" This module tests the review app views """

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
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

        Then signs into the 'johndoe' user created in the setUp method,
        passing user authentication, before collecting the response of
        the get 'my_reviews' view. Uses Django's inbuilt HTTP client to
        ensure a status code 200 is returned and the template used is
        the correct one.

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

    def test_delete_review_removes_specified_object(self):
        """
        A test to ensure the delete_review view removes the review
        that is passed to it.

        Collects all the objects in the Reviews database, asserting the total
        length is 2, this is for use in making comparisons later. Then
        collects the Product created in the setUp method.

        Then signs into the 'johndoe' user created in the setUp method,
        passing user authentication, before collecting the response of
        the 'delete_review' view when passed with the product ID.
        Uses Django's inbuilt HTTP client to ensure a status code 302,
        a redirect response, is returned and the redirect url is the
        reverse of the 'my_reviews'. view.

        Then uses Django's get_messages to ensure the the response
        returns the correct error message before collecting all
        the objects in the Reviews database again, asserting the total
        length is now 1. Meaning the review relating the the user
        'johndoe' for 'Raspberry Bon Bons' has been deleted.
        """
        reviews = Reviews.objects.all()
        self.assertEqual(len(reviews), 2)

        product = Product.objects.get(id=1)

        self.client.login(
            email="johndoe@email.com",
            password='password',
        )
        response = self.client.post(reverse('delete_review', args=[product.id]))  # noqa: E501

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('my_reviews')))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Deleted your review of {product.name}!')  # noqa: E501

        reviews = Reviews.objects.all()
        self.assertEqual(len(reviews), 1)
