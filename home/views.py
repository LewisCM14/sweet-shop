""" This module handles the views for the home app """

from django.shortcuts import render


def index(request):
    """ Renders the index.html template in the browser """
    return render(request, 'home/index.html')


def faq(request):
    """ Renders the faq.html template in the browser """
    return render(request, 'home/faq.html')


def deliver_info(request):
    """ Renders the deliver_info.html template in the browser """
    return render(request, 'home/deliver_info.html')
