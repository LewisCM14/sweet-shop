""" This module contains the views for the checkout app """

from django.shortcuts import render, redirect, reverse, get_object_or_404  # noqa: E501
from django.contrib import messages
from django.conf import settings

import stripe

from cart.contexts import cart_contents
from products.models import Product
from .order_form import OrderForm
from .models import OrderLineItem, Order


# pylint: disable=no-member
def checkout(request):
    """
    The view to handle the checkout functionality.
    Takes in the stripe public & secret key from settings.py

    On the GET request:
    Collects the cart dict that is stored in the session.
    Collects the grand total that has been calculated by the
    context processor in the cart app, returning the value
    in 'stripe_total' as the required integer for billing.

    Sets the secret_key on the stripe API and creates the payment intent
    using the stripe_total and STRIPE_CURRENCY from settings.py

    Returns the OrderForm to the checkout template.

    On the POST request:
    Collects the cart from the session.
    Stores the form data in a dict, then passes it to the OrderForm.
    Checks if the then created order_form variable is valid.
    If invalid returns an error message to the user and returns them to
    the checkout page.

    If valid iterates over each item in the cart within a try/except
    to create an OrderLineItem instance for each one. Returns the user
    to the shopping cart if the OrderLineItem creation fails.
    Once the order creation has been complete checks if the user wanted
    to save/update their details, saving this information in the session
    if so and then redirecting to the checkout success page.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, quantity in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "  # noqa: E501
                        "Please contact us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_cart'))
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))  # noqa: E501
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your cart at the moment")  # noqa: E501
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


def checkout_success(request, order_number):
    """
    The view to handle successful checkouts.

    First check the session to see if the the 'save_info' dict
    is stored within it, saving this information in the save_info
    object if so.

    Then collects the order created in the checkout view via it's
    order_number, storing it in order object and passing it to the
    template context before presenting a success message to the user
    and deleting the 'cart' key from the session.
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
