""" This module contains the views for the checkout app """

import json

from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse  # noqa: E501
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.conf import settings

import stripe

from cart.contexts import cart_contents
from products.models import Product
from profiles.models import UserProfile
from profiles.profile_form import UserProfileForm
from .order_form import OrderForm
from .models import OrderLineItem, Order


@require_POST
def cache_checkout_data(request):
    """
    A view to handle caching the data if the user checked the
    save info box.

    Before the confirmCardPayment method in the
    stripe JavaScrip is called. A POST request is made to this view,
    with the client secret from the payment intent.
    That is then split at the word 'secret',
    in order to collect the payment intent ID (pid).

    Stripe is then setup with the secret key,
    so that the payment intent can be modified, with the method
    stripe.PaymentIntent.modify, once passed the pid,
    the metadata which required editing it set:
    Add the user who's placing the order.
    Add whether or not they wanted to save their information.
    Add a JSON dump of their shopping cart.

    If this process fails an error message is returned to the user.
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:  # noqa: F841
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    The view to handle the checkout functionality.
    Takes in the stripe public & secret key from settings.py

    On the GET request:
    Collects the cart dict that is stored in the session.
    Collects the grand total that has been calculated by the
    context processor in the cart app, returning the value
    in 'stripe_total' as the required integer for billing.

    Sets the secret_key on the stripe API and creates the payment intent
    using the stripe_total and STRIPE_CURRENCY from settings.py

    Then checks if the user is authenticated, if so, provided they
    have default delivery information saved on their UserProfile
    returns the OrderForm pre-filled to the checkout template,
    if not authenticated or no default info a blank form is returned.

    On the POST request:
    Collects the cart from the session.
    Stores the form data in a dict, then passes it to the OrderForm.
    Checks if the then created order_form variable is valid.
    If invalid returns an error message to the user and returns them to
    the checkout page.

    If valid, saves the order without committing, collects
    the client_secret from the input on the form storing it in
    the stripe_pid object and then collects the shopping cart
    dumping it into the original_cart object as a JSON string.
    Then finally commits the form.

    Then iterates over each item in the cart within a try/except
    to create an OrderLineItem instance for each one. Returns the user
    to the shopping cart if the OrderLineItem creation fails.
    Once the order creation has been complete checks if the user wanted
    to save/update their details, saving this information in the session
    if so and then redirecting to the checkout success page.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()
            for item_id, quantity in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "  # noqa: E501
                        "Please contact us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_cart'))
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(
                reverse('checkout_success', args=[order.order_number])
            )
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(
                request, "There's nothing in your cart at the moment"
            )
            return redirect(reverse('products'))
        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )
        order_form = OrderForm()

        # Pre-fills the OrderForm with the users saved delivery info if stored.
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'town_or_city': profile.default_town_or_city,
                    'county': profile.default_county,
                    'postcode': profile.default_postcode,
                    'country': profile.default_country,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    # Returns a message to the user if no key set
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    The view to handle successful checkouts.

    First check the session to see if the the 'save_info' dict
    is stored within it, saving this information in the save_info
    object if so.

    Then checks if the user is authenticated and if so collects
    their UserProfile in order to save the order to it via the
    user_profile foreign key on the Order model.

    If the user checked to save_info the UserProfile is then
    updated via the UserProfileForm via the passed in values for
    order delivery.

    Then collects the order created in the checkout view via it's
    order_number, storing it in order object and passing it to the
    template context before presenting a success message to the user
    and deleting the 'cart' key from the session.
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
