""" This module contains the urls for the profiles app """

from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('change_name', views.change_name, name='change_name'),
    path(
        'order_history/<order_number>', views.order_history,
        name='order_history'
    ),
]
