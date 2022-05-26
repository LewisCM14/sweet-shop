""" This module handles the views for the inquiry app """

from django.shortcuts import render
from profiles.models import UserProfile
from .contact_form import ContactForm


def contact_us(request):
    """
    Renders the contact_us.html template in the browser.

    Handles pre-filling sections of the OrderForm by
    collecting the users full name and email if they are
    authenticated, and if they have a UserProfile collecting their
    default phone number. Returns a blank form of none of this information
    is stored.
    """

    user = request.user
    if user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=user)
            contact_form = ContactForm(initial={
                'full_name': user.get_full_name(),
                'email': profile.user.email,
                'phone_number': profile.default_phone_number,
            })
        except UserProfile.DoesNotExist:
            contact_form = ContactForm()
    else:
        contact_form = ContactForm()

    template = 'inquiry/contact_us.html'

    context = {
        'contact_form': contact_form,
    }

    return render(request, template, context)
