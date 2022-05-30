""" This module configures the profiles app """

from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """ app configuration """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'
