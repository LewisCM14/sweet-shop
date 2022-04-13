""" This module handles the views for the products app """

from django.shortcuts import render
from .models import Product


def all_products(request):
    """ A view to show all products """
    # pylint: disable=no-member
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)
