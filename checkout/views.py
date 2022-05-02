""" This module contains the views for the checkout app """

from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.conf import settings

import stripe

from cart.contexts import cart_contents
from .order_form import OrderForm


def checkout(request):
    """
    The view to handle the checkout functionality.

    Takes in the stripe public & secret key from settings.py
    Then the cart dict that is stored in the session.
    Collects the grand total that has been calculated by the
    context processor in the cart app, returning the value
    in 'stripe_total' as the required integer for billing.

    Sets the secret_key on the stripe API and creates the payment intent
    using the stripe_total and STRIPE_CURRENCY from settings.py

    Returns the OrderForm to the checkout template.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('products'))

    current_cart = cart_contents(request)
    total = current_cart['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

    order_form = OrderForm()

    # Returns a message to the user if no key set
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
