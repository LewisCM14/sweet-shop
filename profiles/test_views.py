""" This module tests the profile app views """

from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class TestModel(TestCase):
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
        Uses Django's in-built HTTP client to get the profile page URL.
        Asserts equal to status code 200, a successful HTTP response.
        """
        self.login()
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
