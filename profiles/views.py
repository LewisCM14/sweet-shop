""" This module contains the views for the profiles app """

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .profile_form import UserProfileForm


# pylint: disable=redefined-outer-name
@login_required
def profile(request):
    """
    Renders the user profile in the profile.html template.

    Uses get_object_or_404 to fetch the current signed in
    users profile from the UserProfile model, stores this in
    the profile variable. This variable is then used to
    populate the UserProfileForm.

    Upon a POST request, checks the form is valid and if so,
    updates it.
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:  # return the form data back to the view if form not valid
            messages.error(request, 'Update failed. Please ensure the form is valid.')  # noqa: E501
    else:
        form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'hide_cart': True,
    }

    return render(request, template, context)
