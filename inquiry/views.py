""" This module handles the views for the inquiry app """

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
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

    On the POST request collects the form data and passes it to the
    ContactFrom, if invalid the form is returned to the user with the errors
    displayed. If valid, the instance is saved without committing and the
    users authentication status is checked, if the request was made by an
    authorized user their ID is attached to the inquiry before it is
    posted to the database. If not the form is posted with that field blank.
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

    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'subject': request.POST['subject'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'message': request.POST['message'],
        }
        contact_form = ContactForm(form_data)
        if contact_form.is_valid():
            inquiry = contact_form.save(commit=False)
            if user.is_authenticated:
                inquiry.user = request.user
                inquiry.save()
            else:
                inquiry.save()
            messages.info(request, 'Your inquiry has been sent. \
                We will be in touch as soon as possible.')
            return redirect(reverse('mail_success'))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check the information you provided.')

    template = 'inquiry/contact_us.html'

    context = {
        'contact_form': contact_form,
    }

    return render(request, template, context)


def mail_success(request):
    """ A view to render the main success template """
    return render(request, 'inquiry/mail_success.html')
