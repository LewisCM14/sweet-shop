"""
This module tells Django about the custom ready method in apps.py,
allowing the signals.py module to preform as intended.
"""

default_app_config = 'checkout.apps.CheckoutConfig'
