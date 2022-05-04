""" This module configures the checkout app """

from django.apps import AppConfig


# pylint: disable=unused-import
class CheckoutConfig(AppConfig):
    """ configuration settings for the checkout app."""
    name = 'checkout'

    # pylint: disable=import-outside-toplevel
    def ready(self):
        """
        Import the signals.py module.
        """
        import checkout.signals  # noqa: F401
