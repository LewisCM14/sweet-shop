""" This module handles the views for the products app """

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product


def all_products(request):
    """
    A view to show all products

    Search Functionality:
    Handles the search function in the main nav.
    Takes in the GET request from the form,
    storing the input named as 'q' in the query variable.
    If no value is input, an error message is returned
    and the user is redirected to the prodcuts url.
    If there is a value input, the queries variable is set
    equal to a Q object, where the name or the description,
    contains the query (case insensitive).
    The products variable is then filtered by the queries variable.
    """
    # pylint: disable=no-member
    products = Product.objects.all()
    # Set to none initially to ensure no error is returned in context
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")  # noqa
                return redirect(reverse('products'))

        queries = Q(name__icontains=query) | Q(description__icontains=query)  # noqa
        products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
