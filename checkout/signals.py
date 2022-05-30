""" This module contains the signals used in the checkout app (See init.py) """

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


# See apps.py for how these signals are implemented.
@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    This function handles signals from the post save event on
    the OrderLineItem model. It will ensure each time a
    line item is added or updated to an order the fields
    relating to cost are updated.

    The parameters refer to the:
    Sender of the signal. In this case OrderLineItem.
    The actual instance of the model that sent it, i.e.
    each individual order.
    A boolean sent by django referring to whether
    this is a new instance or one being updated.
    Then any keyword arguments.

    Access instance.order which refers to the order
    this specific line item is related to.
    Then call the update_total Order model method on it.
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    This function handles signals from the post delete event on
    the OrderLineItem model. It will ensure each time a
    line item is removed from an order the fields relating to cost
    are updated.

    The parameters refer to the:
    Sender of the signal. In this case OrderLineItem.
    The actual instance of the model that sent it, i.e.
    each individual order.
    Then any keyword arguments.

    Access instance.order which refers to the order
    this specific line item is related to.
    Then call the update_total Order model method on it.
    """
    instance.order.update_total()
