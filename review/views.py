""" This module handles the views for the review app """

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from products.models import Product
from .models import Reviews
from .review_form import PostReviewForm


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
            messages.error(
                request, f'You have already reviewed {product.name}!'
            )
            return HttpResponseRedirect(
                reverse('product_detail', args=[product.id])
            )
        else:
            form = PostReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = user
                review.product = product
                review.save()
                messages.info(request, 'Thanks for your review!')
            else:
                messages.error(
                    request, 'Review failed. Please ensure the form is valid.'
                )
                form = PostReviewForm()

        return HttpResponseRedirect(
            reverse('product_detail', args=[product.id])
        )


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


@login_required
def delete_review(request, product_id):
    """
    A view to handle users deleting their reviews.

    Collects the product via the product_id passed in
    and the user from the session, before collecting the review
    from the Review database that matches these two fields and
    then calling the delete method on it before reloading the
    'my_reviews' page and retuning a user message.
    """
    product = get_object_or_404(Product, pk=product_id)
    user = request.user

    review = Reviews.objects.get(
        product=product,
        user=user
    )

    review.delete()
    messages.warning(
        request, f'Deleted your review of {product.name}!'
    )

    return HttpResponseRedirect(reverse('my_reviews'))


@login_required
def edit_review(request, review_id):
    """
    A view to handle rendering and updating a specific products review.

    Collects the review object via the passed in review_id,
    asserts the user attached to the review is the same as the
    user making the request, redirecting if not.

    If they match the review is rendered in the PostReviewForm
    on the template and upon a post request, provided the form is
    valid, the review is updated and the user is redirected to their
    reviews. If invalid the form is reloaded to display the errors,
    user feedback messages are provided for either result.
    """

    review = get_object_or_404(Reviews, pk=review_id)

    if review.user != request.user:
        messages.error(
            request, 'You cannot alter this review!'
        )
        return redirect(reverse('my_reviews'))
    else:
        form = PostReviewForm(instance=review)
        if request.method == 'POST':
            form = PostReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, 'Review updated successfully!')
                return redirect(reverse('my_reviews'))
            else:
                messages.error(
                    request, 'Failed to update the review. Please ensure the form is valid.')  # noqa: E501
        else:
            form = PostReviewForm(instance=review)
            messages.info(request, f'You are editing your review of {review.product.name}')  # noqa: E501

        template = 'reviews/edit_review.html'
        context = {
            'review': review,
            'form': form,
        }

        return render(request, template, context)
