""" This module contains the admin logic for the inquiry app """

from django.contrib import admin
from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    """
    The admin class for the Inquiry model.
    """
    list_display = (
        'id',
        'full_name',
        'email',
        'subject',
        'date',
    )

    readonly_fields = (
        'user', 'full_name', 'email', 'subject', 'message', 'date',
    )

    ordering = ('-date',)
