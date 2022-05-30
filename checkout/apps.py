""" This module configures the checkout app """

from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """ configuration settings for the checkout app."""
    name = 'checkout'

    def ready(self):
        """
        Import the signals.py module.
        """
        import checkout.signals  # noqa: F401
