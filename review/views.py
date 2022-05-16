""" This module handles the views for the review app """

from django.shortcuts import render, reverse, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from products.models import Product
from .models import Reviews
from .review_form import PostReviewForm


# pylint: disable=no-member
@login_required
def post_review(request, product_id):
    """
    A view to allow users to post a product review.

    Collects the product object from the Product database
    via the id of the passed in 'product_id' and collects the user
    from the request.

    On the POST request filters the Review database via the user and product,
    if they have already posted a review for that product an error
    message is returned.

    If the check returns no results an instance of the PostReviewForm is
    created and if valid, the user and product are applied and it is saved
    to the database before user feedback is provided and the product_detail
    page is reloaded for the passed in product ID.

    If invalid the form post fails and user feedback is provided.
    """

    product = get_object_or_404(Product, pk=product_id)
    user = request.user

    if request.method == 'POST':
        if Reviews.objects.filter(user=user, product=product,).exists():
            messages.error(request, f'You have already reviewed {product.name}!')  # noqa: E501
            return HttpResponseRedirect(reverse('product_detail', args=[product.id]))  # noqa: E501
        else:
            form = PostReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = user
                review.product = product
                review.save()
                messages.info(request, 'Thanks for your review!')
            else:
                messages.error(request, 'Review failed. Please ensure the form is valid.')  # noqa: E501
                form = PostReviewForm()

        return HttpResponseRedirect(reverse('product_detail', args=[product.id]))  # noqa: E501


@login_required
def my_reviews(request):
    """
    Renders a users reviews in the browser.

    Filters the Reviews database via the user from the request,
    returning them as context to the template for display.
    """
    reviews = Reviews.objects.filter(user=request.user)

    template = 'reviews/my_reviews.html'
    context = {
        'reviews': reviews,
    }

    return render(request, template, context)
