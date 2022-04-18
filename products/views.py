""" This module handles the views for the products app """

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Type


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

    Type Filtering:
    Takes in the type_query from the GET request,
    storing the required type value in the type_filter variable.
    Then filters the products returned in the view by the name value
    of the type_filter. Then converts the list of strings of type names
    passed through the URL into a list of actual type objects,
    so that all their fields can be accessed in the template.
    """
    # pylint: disable=no-member
    products = Product.objects.all()
    # Set to none initially to ensure no error is returned in context
    query = None
    type_filter = None

    if request.GET:
        if 'type_query' in request.GET:
            type_filter = request.GET['type_query'].split(',')
            products = products.filter(type__name__in=type_filter)
            type_filter = Type.objects.filter(name__in=type_filter)

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
        'current_type': type_filter,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
