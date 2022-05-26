""" This module handles the views for the inquiry app """

from django.shortcuts import render
from .contact_form import ContactForm


def contact_us(request):
    """ Renders the contact_us.html template in the browser """

    form = ContactForm()

    template = 'inquiry/contact_us.html'

    context = {
        'contact_form': form,
    }

    return render(request, template, context)
