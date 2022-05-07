""" This module handles the webhooks sent by stripe """

from django.http import HttpResponse


# pylint: disable=invalid-name
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
        Handle the payment_intent.succeeded webhook from Stripe
        """
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
