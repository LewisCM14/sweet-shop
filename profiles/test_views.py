""" This module tests the profile app views """

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile


# pylint: disable=no-member
class TestView(TestCase):
    """
    Contains the tests for the views.
    Located in the profile app in views.py.
    """

    def setUp(self):
        """
        Creates a User test case.
        """
        User.objects.create_user(
            username='johndoe',
            first_name='john',
            last_name='doe',
            email='johndoe@email.com',
            password='password',
        )

    def login(self):
        """
        Helper Method

        Logs into the User created in the setUp method.
        Called in the below tests to pass user authentication conditions.
        """
        self.client.login(
            email="johndoe@email.com",
            password='password',
        )

    def test_get_profile_page(self):
        """
        Tests the profile page renders.

        Uses the login helper method to sign into the test case User.
        Passing the views authentication conditions.
        Uses Django's in-built HTTP client to get the profile page URL.
        Asserts equal to status code 200, a successful HTTP response.
        """
        self.login()
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_user_profile_form_saves(self):
        """
        Tests a valid UserProfileForm instance posts to the database.

        Uses the login helper method to sign into the test case User.
        Passing the views authentication conditions.

        Collects the profile for the user via ID storing it in user_profile,
        then asserts all the fields in this model currently have no value set/

        Posts a valid UserProfileForm instance to the reverse of
        the profile URL. Then uses Django's in-built HTTP client to ensure
        it returns a successful HTTP 200 response.

        Then collects the profile for the user via ID again,
        asserting all the fields in this model now have values equal to the
        data passed in the POST request.
        """
        self.login()
        user_profile = UserProfile.objects.get(id=1)

        self.assertEqual(user_profile.default_phone_number, None)
        self.assertEqual(user_profile.default_street_address1, None)
        self.assertEqual(user_profile.default_street_address2, None)
        self.assertEqual(user_profile.default_town_or_city, None)
        self.assertEqual(user_profile.default_county, None)
        self.assertEqual(user_profile.default_postcode, None)
        self.assertEqual(user_profile.default_country, None)

        response = self.client.post(
            reverse("profile"), {
                'default_phone_number': '11111111111',
                'default_street_address1': '4 privet drive',
                'default_street_address2': '',
                'default_town_or_city': 'little whinging',
                'default_county': 'surrey',
                'default_postcode': 'CR2 5ER',
                'default_country': 'GB',
            })
        self.assertEqual(response.status_code, 200)

        user_profile = UserProfile.objects.get(id=1)

        self.assertEqual(user_profile.default_phone_number, '11111111111')
        self.assertEqual(user_profile.default_street_address1, '4 privet drive')  # noqa: E501
        self.assertEqual(user_profile.default_street_address2, '')
        self.assertEqual(user_profile.default_town_or_city, 'little whinging')
        self.assertEqual(user_profile.default_county, 'surrey')
        self.assertEqual(user_profile.default_postcode, 'CR2 5ER')
        self.assertEqual(user_profile.default_country, 'GB')
