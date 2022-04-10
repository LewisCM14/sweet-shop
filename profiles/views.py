""" This module contains the views for the profiles app """

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm


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

    NEED TO ADD TOASTS FOR MESSAGES AND ADD ON PROFILE PAGE = TRUE TO CONTEXT
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
    else:  # return the form data back to the view if form not valid
        form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
