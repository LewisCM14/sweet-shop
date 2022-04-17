""" This module contains the urls for the home app """

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('faq/', views.faq, name='faq'),
    path('delivery-information/', views.deliver_info, name='deliver_info'),
]
