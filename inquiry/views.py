""" This module handles the views for the inquiry app """

from django.shortcuts import render


def contact_us(request):
    """ Renders the contact_us.html template in the browser """
    return render(request, 'inquiry/contact_us.html')
