""" This module handles the views for the favorites app """

from django.shortcuts import render, reverse, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from products.models import Product
from .models import Favorites


@login_required
def check_favorite(request, product_id):
    """
    A view to allow users to add or remove products from their favorites.

    On the GET request, uses the passed in product_id value
    to collect the product object from the database and collects the user
    from the session, filtering the Favorites database via these fields.

    If that object exists, it is collected, stored and then deleted,
    if it doesn't exist it is created. User feedback is returned in
    either instance and a Http redirect response is returned in order
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
            messages.warning(
                request, f'Removed {product.name} from your favorites!'
            )
        else:
            Favorites.objects.create(
                product=product,
                user=user
            )
            messages.info(
                request, f'Added {product.name} to your favorites!'
            )

        return HttpResponseRedirect(
            reverse('product_detail', args=[product.id])
        )


@login_required
def view_favorite(request):
    """
    Renders the view_favorites.html template in the browser

    Collects all the objects in the Favorites database that match
    the user who made the request, returning them to the template
    as context.
    """
    favorites = Favorites.objects.filter(user=request.user)

    template = 'favorites/view_favorites.html'
    context = {
        'favorites': favorites,
    }

    return render(request, template, context)


@login_required
def remove_favorite(request, product_id):
    """
    A view to handle users removing products from their favorites list.

    On the request, uses the passed in product_id value
    to collect the product object from the database and collects the user
    from the session. Then collects the object that matches these
    two values from the Favorites database and deletes it,
    returning a user feedback message before reloading the page.
    """
    product = get_object_or_404(Product, pk=product_id)
    user = request.user

    favorites = Favorites.objects.get(
        product=product,
        user=user
    )

    favorites.delete()
    messages.warning(
        request, f'Removed {product.name} from your favorites!'
    )

    return HttpResponseRedirect(reverse('my_favorites'))
