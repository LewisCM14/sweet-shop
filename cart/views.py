""" This module handles the views for the cart app """

from django.shortcuts import render


def view_cart(request):
    """ Renders the cart.html template in the browser """
    return render(request, 'cart/cart.html')
