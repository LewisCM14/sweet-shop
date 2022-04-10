""" This module contains the views for the profiles app """

from django.shortcuts import render


def profile(request):
    """
    Renders the user profile
    """
    template = 'profiles/profile.html'
    context = {}

    return render(request, template, context)
