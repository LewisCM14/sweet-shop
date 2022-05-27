""" This module contains the urls for the inquiry app """

from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_us, name='contact_us'),
    path('mail_success/', views.mail_success, name='mail_success'),
]
