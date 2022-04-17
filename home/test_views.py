""" This module tests the home app views """

from django.test import TestCase


class TestModel(TestCase):
    """
    Contains the tests for the views.
    Located in the home app in views.py.
    """

    def test_get_index_page(self):
        """
        Tests the index page renders.

        Uses Django's in-built HTTP client to get the index page URL.
        Asserts equal to status code 200, a successful HTTP response.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)