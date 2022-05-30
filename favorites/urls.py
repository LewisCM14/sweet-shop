""" This module contains the urls for the profiles app """

from django.urls import path
from . import views

urlpatterns = [
    path('check/<product_id>', views.check_favorite, name='favorite'),
    path('my_favorites/', views.view_favorite, name='my_favorites'),
    path('remove/<product_id>', views.remove_favorite, name='remove_favorite')
]
