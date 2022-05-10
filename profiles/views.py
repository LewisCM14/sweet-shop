""" This module contains the views for the profiles app """

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from checkout.models import Order

# from checkout.models import Order

from .models import UserProfile
from .profile_form import UserProfileForm


# pylint: disable=redefined-outer-name
@login_required
def profile(request):
    """
    A view to handle rendering and updating the user profile.

    Collects the current user with request.user for use
    when updating the first & last name fields of the User model,
    stored in the user variable.

    Then uses get_object_or_404 to fetch the current signed in
    users profile from the UserProfile model, stores this in
    the profile variable.

    The UserProfileForm is then populated with the relevant from_data.

    Upon a POST request, checks if the form is valid and if so,
    updates the first_name and last_name fields on the User
    model to the updated values and then updates the UserProfile
    with the passed in form inputs.
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')  # noqa: E501
    else:  # return the form data back to the view if form not valid
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'hide_cart': True,
    }

    return render(request, template, context)


@login_required
def change_name(request):
    """ a view to handle users changing their name """
    return render(request, 'profiles/name_change.html')


def order_history(request, order_number):
    """
    A view to handle displaying a users order history.

    Collects the Order instance via its order_number,
    from the profile view, before adding a message letting
    the user know they're looking at a past order confirmation.
    Then using the checkout_success template, renders the
    order confirmation.

    The from_profile variable within the context us used
    to implement navigation back to the profile page if that is
    the original location the user arrived from.
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
