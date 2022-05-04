""" This module tests the profile app views """

from django.test import TestCase
from django.contrib.auth.models import User
from .profile_form import UserProfileForm


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
            email="johndoe@email.com",
            password='password',
        )

    def login(self):
        """
        Helper Method

        Logs into the User created in the setUp method.
        Called in the below tests to pass user authentication conditions.
        """
        self.client.login(
            username='johndoe',
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
        Creates an instance of the UserProfileForm stored in the form variable,
        asserts this instance of the form is valid. Then asserts this form
        instance posts to the database.
        Then uses Django's in-built HTTP client
        to ensure it returns a successful HTTP 200 response.
        """
        self.login()
        form = UserProfileForm(data={
            'default_forname': 'john',
            'default_surname': 'doe',
            'default_phone_number': '1111111111111111',
            'default_street_address1': '4 privet drive',
            'default_street_address2': '',
            'default_town_or_city': 'little whinging',
            'default_county': 'surrey',
            'default_postcode': 'CR2 5ER',
        })
        self.assertTrue(form.is_valid())
        response = self.client.post('/profile/', {'form': form})
        self.assertEqual(response.status_code, 200)
