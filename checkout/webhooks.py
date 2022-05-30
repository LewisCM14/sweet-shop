""" This module contains the webhook for stripe payment intents """


from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

import stripe

from checkout.webhook_handler import StripeWH_Handler


@require_POST
@csrf_exempt
def webhook(request):
    """
    The function to handle listening for stripes webhooks.
    Decorated with require_POST to prevent a GET request and
    csrf_exempt as Stripe doesn't send a csrf token.

    Modifying the webhook view to use the webhook handler:
    Create an instance of the WH handler, passing in the request.
    Then create a dictionary called event_map
    the keys will be the names of the webhooks coming from stripe,
    while its values will be the actual methods inside the handler.

    Get the type of event from stripe, which will be stored in the key 'type'.

    Then look up the key in the dict and assign its value
    to a variable called event handler, at this point event_handler
    is nothing more than an alias for the function pulled from the dict.

    Call the event_handler, passing it the 'event' and return the
    'response' to Stripe, i.e call the the function for handling the
    specific event triggered by stripe's payment intent.
    """
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:  # noqa: F841
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:  # noqa: F841
        # Invalid signature
        return HttpResponse(status=400)
        # General error catching
    except Exception as e:
        return HttpResponse(content=e, status=400)

    # Set up a webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,  # noqa: E501
    }

    # Get the webhook type from Stripe
    event_type = event['type']

    # If there's a handler for it, get it from the event map
    # Use the generic one by default
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event
    response = event_handler(event)
    return response
