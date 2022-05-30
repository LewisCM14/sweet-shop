""" This module tests the home app views """

from django.test import TestCase


class TestView(TestCase):
    """
    Contains the tests for the views.
    Located in the home app in views.py.
    """

    def test_get_index_page(self):
        """
        Tests the index page renders.

        Uses Django's in-built HTTP client to get the index page URL.
        Asserts equal to status code 200, a successful HTTP response.
        Then asserts the correct template is used.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ('home/index.html'))

    def test_get_faq_page(self):
        """
        Tests the faq page renders.

        Uses Django's in-built HTTP client to get the faq page URL.
        Asserts equal to status code 200, a successful HTTP response.
        Then asserts the correct template is used.
        """
        response = self.client.get('/faq/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ('home/faq.html'))

    def test_get_deliver_info_page(self):
        """
        Tests the delivery information page renders.

        Uses Django's in-built HTTP client to get the delivery info page URL.
        Asserts equal to status code 200, a successful HTTP response.
        Then asserts the correct template is used.
        """
        response = self.client.get('/delivery-information/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ('home/deliver_info.html'))

    def test_get_about_us_page(self):
        """
        Tests the about us page renders.

        Uses Django's in-built HTTP client to get the index page URL.
        Asserts equal to status code 200, a successful HTTP response.
        Then asserts the correct template is used.
        """
        response = self.client.get('/about_us/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ('home/about_us.html'))

    def test_get_privacy_policy_page(self):
        """
        Tests the privacy page renders.

        Uses Django's in-built HTTP client to get the privacy page URL.
        Asserts equal to status code 200, a successful HTTP response.
        Then asserts the correct template is used.
        """
        response = self.client.get('/privacy_policy/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ('home/privacy_policy.html'))
