""" This module handles the views for the cart app """

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from products.models import Product


def view_cart(request):
    """ Renders the cart.html template in the browser """
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """
    The function to handle adding items to the cart.

    All data is posted from the form on product_details.html
    The cart itself is stored within the http session.

    Collects the product being added for use in toasts.
    Collects the quantity from the form converting it to a integer
    Collects the redirect url.
    collects the cart instance from the session or creates one.

    Checks if the passed item_id is in the cart dictionary,
    incrementing by the provided quantity if so, or adding if not.
    The updated cart variable is then placed into the session.
    User feedback messages are returned at either point.
    The user is then redirected to the provided url (the product_detail page).
    """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}')  # noqa
    else:
        cart[item_id] = quantity
        messages.success(request, f'Added {product.name} to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """
    Handles adjusting the items in the cart
    """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}')  # noqa
    else:
        cart.pop(item_id)
        messages.success(request, f'Removed {product.name} from your cart')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))
