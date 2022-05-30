""" This module configures the home app """

from django.apps import AppConfig


class HomeConfig(AppConfig):
    """ app configuration """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
