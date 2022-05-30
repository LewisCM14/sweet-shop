""" This module configures the cart app """

from django.apps import AppConfig


class CartConfig(AppConfig):
    """ cart app configuration """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
