""" This module handles the views for the cart app """

from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404  # noqa: E501
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
        messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}')  # noqa: E501
    else:
        cart[item_id] = quantity
        messages.success(request, f'Added {product.name} to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """
    A function to handle adjusting the items within the cart.

    All data is posted from the form on cart.html
    The cart itself is stored within the http session.

    Collects the product being added for use in toasts.
    Collects the quantity from the form converting it to a integer
    collects the cart instance from the session or creates one.

    Checks if the passed quantity is greater than 0,
    updating the quantity of the item_id by the provided integer if so.
    If the passed quantity is not greater than 0,
    the item_id within the cart is passed to the pop method, removing it.
    User feedback messages are returned at either point.
    The user is then redirected back to the cart view.
    """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}')  # noqa: E501
    else:
        cart.pop(item_id)
        messages.success(request, f'Removed {product.name} from your cart')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """
    A function to handle removing the items within the cart.
    """

    try:
        product = get_object_or_404(Product, pk=item_id)
        cart = request.session.get('cart', {})

        cart.pop(item_id)
        messages.success(request, f'Removed {product.name} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    # pylint: disable=broad-except
    except Exception as error:
        messages.error(request, f'Error removing item: {error}')
        return HttpResponse(status=500)
