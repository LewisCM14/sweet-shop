""" This module contains the URLS for the checkout app """

from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
]
