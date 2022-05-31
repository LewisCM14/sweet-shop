""" This module handles the views for the home app """

from django.shortcuts import render
from products.models import Product


def index(request):
    """
    A view to renders the index.html template in the browser.

    Filters the Product database via the type field,
    returning the results to to context for use in display
    """
    products = Product.objects.all()
    sour = Product.objects.filter(type=6)
    fizzy = Product.objects.filter(type=5)
    chocolate = Product.objects.filter(type=4)
    chewy = Product.objects.filter(type=3)
    sherbet = Product.objects.filter(type=2)
    jellies_gums = Product.objects.filter(type=1)

    template = 'home/index.html'

    context = {
        'products': products,
        'chewy': chewy,
        'fizzy': fizzy,
        'chocolate': chocolate,
        'sour': sour,
        'sherbet': sherbet,
        'jellies_gums': jellies_gums,
    }

    return render(request, template, context)


def faq(request):
    """ Renders the faq.html template in the browser """
    return render(request, 'home/faq.html')


def deliver_info(request):
    """ Renders the deliver_info.html template in the browser """
    return render(request, 'home/deliver_info.html')


def about_us(request):
    """ Renders the about_us.html template in the browser """
    return render(request, 'home/about_us.html')


def privacy_policy(request):
    """ Renders the privacy_policy.html template in the browser """
    return render(request, 'home/privacy_policy.html')
