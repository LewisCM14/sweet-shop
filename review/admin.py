""" This module contains the admin logic for the review app """

from django.contrib import admin
from .models import Reviews


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """
    The admin class for the Reviews model.
    """
    list_display = (
        'user',
        'product',
        'rating',
        'added_on',
    )

    list_filter = (
        'product',
        'rating',
    )

    ordering = ('added_on',)
