""" This module handles the views for the review app """

from django.shortcuts import reverse, get_object_or_404
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
