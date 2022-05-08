""" This module contains the admin logic for the checkout app """

from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """
    This admin is registered in OrderAdmin.

    Inline item, allow add and edit line items in the admin,
    from inside the order model.
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total', 'lineitem_weight')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    The admin class for the Order model.

    Read only fields calculated by model methods.
    Fields are specified to ensure the order
    stays the same as it appears in the model.

    Ordered by date in reverse chronological order.
    """
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'order_weight', 'grand_total',
                       'original_cart', 'stripe_pid',)

    fields = ('order_number', 'user_profile', 'full_name',
              'email', 'phone_number', 'street_address1',
              'street_address2', 'town_or_city',  'county',
              'postcode', 'country', 'date', 'order_total',
              'order_weight', 'delivery_cost', 'grand_total',
              'original_cart', 'stripe_pid',)

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',)
