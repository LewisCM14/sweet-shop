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

    Allows site admins to manage Order status
    from within the dropdown menu.

    Read only fields calculated by model methods.
    Fields are specified to ensure the order
    stays the same as it appears in the model.

    Ordered by date in reverse chronological order.
    """
    inlines = (OrderLineItemAdminInline,)
    actions = ['package_order', 'post_order', 'process_order']

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'order_weight', 'grand_total',
                       'original_cart', 'stripe_pid',)

    fields = ('order_number', 'user_profile', 'full_name',
              'email', 'phone_number', 'street_address1',
              'street_address2', 'town_or_city',  'county',
              'postcode', 'country', 'date', 'order_total',
              'order_weight', 'delivery_cost', 'grand_total',
              'original_cart', 'stripe_pid', 'status',)

    list_display = ('status', 'order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',)

    def package_order(self, _request, queryset):
        """
        Allows the status field on Orders to be updated to packaged
        from the admin dropdown menu.
        """
        for order in queryset:
            order.status = 1
            order.save()

    def post_order(self, _request, queryset):
        """
        Allows the status field on Orders to be updated to posted
        from the admin dropdown menu.
        """
        for order in queryset:
            order.status = 2
            order.save()

    def process_order(self, _request, queryset):
        """
        Allows the status field on Orders to be updated to processing
        from the admin dropdown menu.
        """
        for order in queryset:
            order.status = 0
            order.save()
