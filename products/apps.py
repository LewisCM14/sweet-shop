""" This module configures the products app """

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """ app configuration """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
