""" This module contains the context processor for the cart app. """

from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.conf import settings
from products.models import Product


def cart_contents(request):
    """
    A custom context processor for making the cart contents global.

    Initiates the cart_items list, used for template logic.
    Sets the total, combined_weight & product_count variables to 0.
    collects/initializes the cart from the http session.

    Iterates over each item stored within the 'cart' session, incrementing
    the total and combined_weight variables based upon the items * quantity.
    Then increments the total product_count based upon the amount of
    individual items. Before appending a dictionary to 'cart_items'
    containing the item_id, quantity, and product object itself.
    Providing access to all other fields from the Product model
    when iterating through the cart_items in templates.

    Calculates the delivery cost based upon the total & combined weight
    of the products within the cart. Utilizes the FREE_DELIVERY_THRESHOLD
    variable located in settings.py. This is wrapped in an if/else statement
    to prevent the cart contents base html being displayed in success toast
    if there is no items stored in the session.
    """
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})
    combined_weight = 0

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        combined_weight += quantity * product.weight_in_grams
        product_count += quantity
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if len(cart_items) > 0:
        if total < settings.FREE_DELIVERY_THRESHOLD:
            if combined_weight + 100 < 1000:
                delivery = Decimal(2.49)
                free_delivery_delta = Decimal(
                    settings.FREE_DELIVERY_THRESHOLD - total
                )
            elif combined_weight + 100 > 1000:
                delivery = Decimal(3.49)
                free_delivery_delta = Decimal(
                    settings.FREE_DELIVERY_THRESHOLD - total
                )
        else:
            delivery = 0
            free_delivery_delta = 0

        grand_total = delivery + total
    else:
        free_delivery_delta = None
        delivery = None
        grand_total = None

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
