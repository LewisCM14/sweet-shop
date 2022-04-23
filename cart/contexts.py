""" This module contains the context processor for the cart app. """

from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.conf import settings
from products.models import Product


def cart_contents(request):
    """
    Makes the cart contents dictionairy avaliable globally
    """
    cart_items = []
    total = 0
    product_count = 0
    weight = 100  # REMOVE LATER

    if total < settings.FREE_DELIVERY_THRESHOLD:
        if weight + 100 < 1000:
            delivery = 2.49
            free_delivery_delta = Decimal(settings.FREE_DELIVERY_THRESHOLD - total)  # noqa
        elif weight + 100 > 1000:
            delivery = 3.49
            free_delivery_delta = Decimal(settings.FREE_DELIVERY_THRESHOLD - total)  # noqa
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
