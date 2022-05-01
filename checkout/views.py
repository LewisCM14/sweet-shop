""" This module contains the views for the checkout app """

from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from .order_form import OrderForm


def checkout(request):
    """ The view to display the checkout section """
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'

    context = {
        'order_form': order_form,
    }

    return render(request, template, context)
