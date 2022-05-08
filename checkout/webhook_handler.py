""" This module handles the webhooks sent by stripe """

import json
import time

from django.http import HttpResponse

from products.models import Product
from .models import Order, OrderLineItem


# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=broad-except
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

        The order_exists boolean is then set to false and the attempt
        counter set to 5. Then within a while loop the webhook checks
        if the Order instance already exists within the database.
        If so breaks out of the loop and returns a HttpResponse 200.

        Once the counter reaches 0 'order_exists' is set to False and the
        Order instance is created from within the webhook using
        the data collected in the shipping_details variable, before
        returning a HttpResponse 200.

        If the Order can not be found or created from within the webhook a
        HttpResponse 500 is returned along with the error message.

        To ensure each Order instance is unique the original_cart and
        stripe_pid fields are used, the stripe_pid value will always
        be unique.
        """
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        # save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',  # noqa
                    status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                for item_id, quantity in json.loads(cart).items():
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',  # noqa: E501
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
