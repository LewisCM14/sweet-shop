""" This module configures the review app """

from django.apps import AppConfig


class ReviewConfig(AppConfig):
    """ app configuration """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'review'
