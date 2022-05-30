""" This module tests the inquiry app models """

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Inquiry


class TestModel(TestCase):
    """
    Contains the tests for the Inquiry model.
    Located in the inquiry app in models.py.
    """

    def setUp(self):
        """
        Creates a test user.
        """

        User.objects.create_user(
            username='johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@email.com',
            password='password',
        )

    def test_inquiry_string_method_return(self):
        """
        Tests the string method on the Inquiry model.

        Collects the User created in the setUp method.
        Then uses it to create an object in the Inquiry database,
        before asserting the str value of this object is correct.
        """

        user = User.objects.get(id=1)

        inquiry = Inquiry.objects.create(
            user=user,
            full_name='John Doe',
            email='johndoe@email.com',
            subject='Test',
            message='A test inquiry',
        )

        self.assertEqual(
            str(inquiry),
            f'{inquiry.full_name} opened {inquiry.subject} on { inquiry.date }'
            )

        self.assertEqual(
            str(inquiry),
            f'John Doe opened Test on {inquiry.date}')
