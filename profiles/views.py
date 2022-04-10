""" This module contains the views for the profiles app """

from django.shortcuts import render, get_object_or_404

from .models import UserProfile
from .forms import UserProfileForm


# pylint: disable=redefined-outer-name
def profile(request):
    """
    Renders the user profile in the profile.html template.

    Uses get_object_or_404 to fetch the current signed in
    users profile from the UserProfile model before
    returning it in the context.
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
