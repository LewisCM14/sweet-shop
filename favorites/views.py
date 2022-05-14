""" This module handles the views for the favorites app """

from django.shortcuts import render, reverse, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from products.models import Product
from .models import Favorites


# pylint: disable=no-member
@login_required
def check_favorite(request, product_id):
    """
    A view to allow users to add or remove products from their favorites.

    On the GET request, uses the passed in product_id value
    to collect the product object from the database and collects the user
    from the session, filtering the Favorites database via these fields.

    If that object exists, it is collected, stored and then deleted,
    if it doesn't exist it is created. User feedback is returned in
    either instace and a Http redirect response is returned in order
    to reload the product_detail page.
    """

    product = get_object_or_404(Product, pk=product_id)
    user = request.user

    if request.method == 'GET':
        if Favorites.objects.filter(user=user, product=product,).exists():
            favorites = Favorites.objects.get(
                product=product,
                user=user
            )
            favorites.delete()
            messages.warning(request, f'Removed {product.name} from your favorites!')  # noqa: E501
        else:
            Favorites.objects.create(
                product=product,
                user=user
            )
            messages.info(request, f'Added {product.name} to your favorites!')  # noqa: E501

        return HttpResponseRedirect(reverse('product_detail', args=[product.id]))  # noqa: E501


@login_required
def view_favorite(request):
    """ Renders the view_favorites.html template in the browser """
    return render(request, 'favorites/view_favorites.html')
