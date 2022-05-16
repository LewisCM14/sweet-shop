""" This module contains the urls for the review app """

from django.urls import path
from . import views

urlpatterns = [
    path('post/<product_id>', views.post_review, name='post_review'),  # noqa: E501
    path('my_reviews/', views.my_reviews, name='my_reviews'),
]
