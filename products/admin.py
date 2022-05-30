""" This module contains the admin logic for the product app """

from django.contrib import admin
from .models import Product, Type


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    The admin class for the Products model.
    extends from the base.
    """
    list_display = (
        'name',
        'type',
        'price',
        'image'
    )

    list_filter = (
        'type', 'popular_in_80s', 'popular_in_90s', 'popular_in_00s',
    )

    ordering = ('name',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    """
    The admin class for the Type model.
    extends from the base.
    """
    list_display = (
        'id',
        'friendly_name',
        'name',
    )
