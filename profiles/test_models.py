""" This module tests the profile app models """

from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class TestModel(TestCase):
    """
    Contains the tests for the UserProfile model.
    Located in the profile app in models.py.
    """

    def test_user_profile_string_method_returns_username(self):
        """
        Tests the string method on the UserProfile model.

        Creates a User instance. Then fetches the object created
        in the UserProfile database for this User instance via id,
        storing this in the John variable.
        Then asserts the string method, returned on this variable,
        returns the username of the test case User, which is johndoe.
        """
        User.objects.create_user(
            username='johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@email.com',
            password='password',
        )

        john = UserProfile.objects.get(id=1)
        self.assertEqual(str(john), 'johndoe')

    def test_user_profile_object_is_created(self):
        """
        Tests a UserProfile object is created when a User object is.

        Creates a User instance, then stores the count of objects
        within the UserProfile database in the count variable.
        Then asserts count is equal to 1 As when a User is created,
        a UserProfile instance should be created for them.
        """
        User.objects.create_user(
            username='johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@email.com',
            password='password',
        )

        count = UserProfile.objects.count()
        self.assertEqual(count, 1)
