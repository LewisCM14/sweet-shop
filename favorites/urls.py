""" This module contains the urls for the profiles app """

from django.urls import path
from . import views

urlpatterns = [
    path('check/<product_id>', views.check_favorite, name='favorite'),  # noqa: E501
]
