""" This module contains a function used to calculate the cart subtotal """

from django import template

register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    Returns the correct subtotal price for the cart.

    This function is registered as a template filter with the decorator
    Using the 'register' variable above,
    which is an instance of template.library
    """
    return price * quantity
