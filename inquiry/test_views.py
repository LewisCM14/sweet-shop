""" This module tests the inquiry app views """

from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages

from profiles.models import UserProfile
from .models import Inquiry


class TestView(TestCase):
    """
    Contains the tests for the views.
    Located in the inquiry app in views.py.
    """

    def setUp(self):
        """
        Creates a User for testing with.
        """
        User.objects.create_user(
            username='johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@email.com',
            password='password',
        )

        profile = UserProfile.objects.get(id=1)
        profile.default_phone_number = 1111111111

    def login(self):
        """
        Helper Method

        Logs into the User created in the setUp method.
        """
        self.client.login(
            email="johndoe@email.com",
            password='password',
        )

    def test_get_mail_success_page(self):
        """
        Tests the mail success page renders.

        Uses Django's in-built HTTP client to get the mail success page URL.
        Asserts equal to status code 200, a successful HTTP response.
        Then asserts the correct template is used.
        """
        response = self.client.get('/contact/mail_success/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ('inquiry/mail_success.html'))

    def test_unauthorized_user_can_make_inquiry(self):
        """
        Tests an unauthorized user can make an inquiry.

        Posts a valid inquiry to the reverse of the contact_us URL, stored
        in the response. Then asserts this response has a status code of 302
        and the redirect URL is the mail_success page.

        The Inquiry database is then filtered via the ID for the inquiry
        just created and the fields are asserted to be equal to the values
        passed. With the 'user' field asserted to be None, as it was an
        unauthorized user than made the request.
        """

        response = self.client.post(
            reverse("contact_us"), {
                'full_name': 'Jane Doe',
                'email': 'janedoe@email.com',
                'phone_number': '1111111111',
                'subject': 'Test',
                'message': 'A test inquiry',
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("mail_success"))

        inquiry = Inquiry.objects.get(id=1)
        self.assertEqual(inquiry.user, None)
        self.assertEqual(inquiry.full_name, 'Jane Doe')
        self.assertEqual(inquiry.email, 'janedoe@email.com')
        self.assertEqual(inquiry.phone_number, '1111111111')
        self.assertEqual(inquiry.subject, 'Test')
        self.assertEqual(inquiry.message, 'A test inquiry')
