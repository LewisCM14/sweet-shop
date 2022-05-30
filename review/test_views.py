""" This module tests the review app views """

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

from products.models import Type, Product
from .models import Reviews


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

        sherbet = Type.objects.create(
            name='sherbet_sweets',
            friendly_name='Sherbet Sweets',
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

        Product.objects.create(
            type=sherbet,
            name='Flying Saucers',
            description='A Sweet filled with Sherbet',
            popular_in_80s=True,
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
        collects the 1st Product created in the setUp method.

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
        response = self.client.post(
            reverse('delete_review', args=[product.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('my_reviews')))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), f'Deleted your review of {product.name}!'
        )

        reviews = Reviews.objects.all()
        self.assertEqual(len(reviews), 1)

    def test_valid_product_review_posts_to_database(self):
        """
        A test to ensure a valid product review posts to the database.

        Collects all the objects in the Reviews database, asserting the total
        length is 2, this is for use in making comparisons later. Then
        collects the 2nd Product created in the setUp method.

        Then signs into the 'johndoe' user created in the setUp method,
        passing user authentication, before collecting the response of
        the 'post_review' view when passed with the product ID and
        a valid rating & review field.

        Uses Django's inbuilt HTTP client to ensure a status code 302,
        a redirect response, is returned and the redirect url is the
        reverse of the 'product_details' view.

        Before collecting all the objects in the Reviews database again,
        asserting the total length is now 3 and the str value for the
        review at index 2 is the value of the review just passed in the
        response. Meaning the review has been added to the database.
        """
        reviews = Reviews.objects.all()
        self.assertEqual(len(reviews), 2)

        product = Product.objects.get(id=2)
        self.client.login(
            email="johndoe@email.com",
            password='password',
        )

        response = self.client.post(
            reverse('post_review', args=[product.id]), {
                'rating': 5,
                'review': 'A nice review.'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, (reverse('product_detail', args=[product.id]))
        )

        reviews = Reviews.objects.all()
        self.assertEqual(len(reviews), 3)
        self.assertEqual(str(reviews[2]), 'Flying Saucers rated 5 stars')

    def test_a_user_cannot_post_multiple_reviews_for_a_product(self):
        """
        A test to ensure a user cannot post multiple reviews for the
        same product.

        Collects all the objects in the Reviews database, asserting the total
        length is 2, this is for use in making comparisons later. Then
        collects the 1st Product created in the setUp method.

        Then signs into the 'johndoe' user created in the setUp method,
        passing user authentication, before collecting the response of
        the 'post_review' view when passed with the product ID and
        a rating & review field.

        Uses Django's inbuilt HTTP client to ensure a status code 302,
        a redirect response, is returned and the redirect url is the
        reverse of the 'product_details' view.

        Then uses Django's get_messages to ensure the the response
        returns the correct error message before collecting all
        the objects in the Reviews database again, asserting the total
        length is still 2. Meaning the review wasn't posted to the
        database.
        """
        reviews = Reviews.objects.all()
        self.assertEqual(len(reviews), 2)

        product = Product.objects.get(id=1)
        self.client.login(
            email="johndoe@email.com",
            password='password',
        )

        response = self.client.post(
            reverse('post_review', args=[product.id]), {
                'rating': 3,
                'review': 'An okay review.'
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, (reverse('product_detail', args=[product.id]))
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), f'You have already reviewed {product.name}!'
        )

        reviews = Reviews.objects.all()
        self.assertEqual(len(reviews), 2)

    def test_invalid_reviews_dont_post_to_the_database(self):
        """
        A test to ensure an invalid review doesn't post to the database.

        Collects all the objects in the Reviews database, asserting the total
        length is 2, this is for use in making comparisons later. Then
        collects the 2nd Product created in the setUp method.

        Then signs into the 'johndoe' user created in the setUp method,
        passing user authentication, before collecting the response of
        the 'post_review' view when passed with the product ID and
        an invalid rating field plus a review field.

        Then uses Django's get_messages to ensure the the response
        returns the correct error message before collecting all
        the objects in the Reviews database again, asserting the total
        length is still 2. Meaning the review wasn't posted to the
        database.
        """
        reviews = Reviews.objects.all()
        self.assertEqual(len(reviews), 2)

        product = Product.objects.get(id=2)
        self.client.login(
            email="johndoe@email.com",
            password='password',
        )

        response = self.client.post(
            reverse('post_review', args=[product.id]), {
                'rating': 6,
                'review': 'An invalid review.'
            }
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Review failed. Please ensure the form is valid.'
        )

        reviews = Reviews.objects.all()
        self.assertEqual(len(reviews), 2)

    def test_the_edit_review_view_template(self):
        """
        A test to ensure the edit_review view uses the correct template.

        Collects the 2nd object in the Reviews database before signing into
        the 'janedoe' user created in the setUp method, passing
        user authentication. Then stores the response of the get
        request for the reverse of the 'edit_review' URL when passed
        the reviews ID. Asserting the template used for the response is
        edit_review.html, the desired template.
        """
        review = Reviews.objects.get(id=2)

        self.client.login(
            email="janedoe@email.com",
            password='password',
        )

        response = self.client.get(reverse('edit_review', args=[review.id]))
        self.assertTemplateUsed(response, ('reviews/edit_review.html'))

    def test_the_edit_review_view_updates_object(self):
        """
        A test to ensure the edit_review view updates the specified object.

        Collects the 2nd objects in the Reviews database, asserting the
        values of the rating & review fields for use in making comparisons.

        Then signs into the 'janedoe' user created in the setUp method,
        passing user authentication, before collecting the response of
        the 'edit_review' view when passed with the review ID and
        a valid rating & review field.

        Then uses Django's inbuilt HTTP client to ensure a status code 302,
        a redirect response, is returned and the redirect url is the
        reverse of the 'my_reviews' view.

        Then uses Django's get_messages to ensure the the response
        returns the correct message before collecting the 2nd Reviews
        object again and asserting the rating & review fields have
        been updated to the values passed in the 'edit_review' URL.
        """
        review = Reviews.objects.get(id=2)
        self.assertEqual(review.rating, 1)
        self.assertEqual(review.review, 'A bad review.')

        self.client.login(
            email="janedoe@email.com",
            password='password',
        )

        response = self.client.post(
            reverse('edit_review', args=[review.id]), {
                'rating': 5,
                'review': 'A good review.'
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('my_reviews')))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Review updated successfully!'
        )

        review = Reviews.objects.get(id=2)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.review, 'A good review.')

    def test_users_can_only_edit_their_reviews(self):
        """
        A test to ensure users can only edit their own reviews.

        Collects the 2nd objects in the Reviews database, asserting the
        values of the rating & review fields for use in making comparisons.

        Then signs into the 'johndoe' user created in the setUp method,
        passing user authentication, before collecting the response of
        the 'edit_review' view when passed with the review ID and
        a valid rating & review field.

        Then uses Django's inbuilt HTTP client to ensure a status code 302,
        a redirect response, is returned and the redirect url is the
        reverse of the 'my_reviews' view.

        Then uses Django's get_messages to ensure the the response
        returns the correct error message before collecting the 2nd Reviews
        object again and asserting the rating & review fields have
        not been updated to the values passed in the 'edit_review' URL,
        as 'johndoe' is not the user related to this review.
        """
        review = Reviews.objects.get(id=2)
        self.assertEqual(review.rating, 1)
        self.assertEqual(review.review, 'A bad review.')

        self.client.login(
            email="johndoe@email.com",
            password='password',
        )

        response = self.client.post(
            reverse('edit_review', args=[review.id]), {
                'rating': 5,
                'review': 'A good review.'
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('my_reviews')))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'You cannot alter this review!'
        )

        review = Reviews.objects.get(id=2)
        self.assertEqual(review.rating, 1)
        self.assertEqual(review.review, 'A bad review.')

    def test_edit_review_doesnt_post_invalid_reviews(self):
        """
        A test to ensure the edit_review view does not post
        invalid reviews to the database.

        Collects the 2nd objects in the Reviews database, asserting the
        values of the rating & review fields for use in making comparisons.

        Then signs into the 'janedoe' user created in the setUp method,
        passing user authentication, before collecting the response of
        the 'edit_review' view when passed with the review ID and
        an invalid rating field and a review field.

        Then uses Django's get_messages to ensure the the response
        returns the correct error message before collecting the 2nd Reviews
        object again and asserting the rating & review fields have
        not been updated to the values passed in the 'edit_review' URL.
        """
        review = Reviews.objects.get(id=2)
        self.assertEqual(review.rating, 1)
        self.assertEqual(review.review, 'A bad review.')

        self.client.login(
            email="janedoe@email.com",
            password='password',
        )

        response = self.client.post(
            reverse('edit_review', args=[review.id]), {
                'rating': 6,
                'review': 'An invalid review.'
            }
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Failed to update the review. Please ensure the form is valid.')  # noqa: E501

        review = Reviews.objects.get(id=2)
        self.assertEqual(review.rating, 1)
        self.assertEqual(review.review, 'A bad review.')
