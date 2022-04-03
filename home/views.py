""" This module handles the views for the home app """

from django.shortcuts import render


def index(request):
    """ Renders the index.html template in the browser """
    return render(request, 'home/index.html')
