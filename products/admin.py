""" This module contains the admin logic for the models products app """

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
        'year',
        'price',
        'image'
    )

    list_filter = ('type', 'year',)

    ordering = ('name',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    """
    The admin class for the Type model.
    extends from the base.
    """
    list_display = (
        'friendly_name',
        'name',
    )
