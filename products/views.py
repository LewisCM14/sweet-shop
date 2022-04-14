""" This module handles the views for the products app """

from django.shortcuts import render, get_object_or_404
from .models import Product


def all_products(request):
    """ A view to show all products """
    # pylint: disable=no-member
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
