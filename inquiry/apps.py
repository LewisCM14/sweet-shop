""" This module configures the inquiry app """

from django.apps import AppConfig


class InquiryConfig(AppConfig):
    """ app configuration """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inquiry'
