""" This module handles the webhooks sent by stripe """

from django.http import HttpResponse

from .models import Order


# pylint: disable=invalid-name
# pylint: disable=no-member
class StripeWH_Handler:
    """ The class to handle stripes webhooks """

    def __init__(self, request):
        """
        A setup method that's called every time an instance
        of the class is created. It is used to assign the request
        as an attribute of the class, allowing access to any
        attributes of the request coming from stripe.
        """
        self.request = request

    def handle_event(self, event):
        """
        A method to handle a generic/unknown/unexpected webhook event
        Take the event stripe is sending, then returns an HTTP response,
        indicating it was received.
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe.

        Collects the payment intent data object from the event.
        Then uses this to collect the payment intent ID, the cart
        metadata passed in the cache_checkout_data view as well as
        the save_info object.

        The billing, shipping and grand_total are also then collected,
        The total being calculated to match the stores price format.
        The shipping details object then has any fields saved as
        empty strings set to Null to match the Order model format.
        """
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
