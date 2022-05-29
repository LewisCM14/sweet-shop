""" This module tests the inquiry app views """

from django.test import TestCase


class TestView(TestCase):
    """
    Contains the tests for the views.
    Located in the inquiry app in views.py.
    """

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
