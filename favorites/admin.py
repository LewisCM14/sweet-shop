""" This module contains the admin logic for the favorites app """

from django.contrib import admin
from .models import Favorites


@admin.register(Favorites)
class FavoriteAdmin(admin.ModelAdmin):
    """
    The admin class for the Favorites model.
    """
    list_display = (
        'product',
        'added_on',
        'user',
    )

    list_filter = (
        'product',
    )

    ordering = ('added_on',)
