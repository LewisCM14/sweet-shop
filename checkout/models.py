""" This module contains the models for the checkout app """

from django.db import models
from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile


class Order (models.Model):
    """
    The Order model, handles all orders across the store.

    when a user checks out, use the information they put into the payment form
    to create an order instance. Then iterate through the items in the cart.
    Creating an order line item for each one. Attaching it to the order.
    And updating the delivery cost, order total, and grand total.

    order_number is non editable and randomly generated with a model method.

    user profile is a foreign key to the order model, uses models.SET_NULL
    so if the profile is deleted order history remains in the admin panel.
    field has null & blank True so that users who don't have an account
    can still make purchases. Has a related name of orders.

    Name, email, phone number all reqired. As is a full delivery address.

    The date field is auto added at the time of the order being submitted.

    Delivery cost, order total and grand total are all calculated using a
    model method.
    """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')  # noqa

    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)

    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label="Country *", null=False, blank=False)

    date = models.DateTimeField(auto_now_add=True)

    # Calculated using model methods.
    delivery_cost = models.DecimalField(
        max_digits=4, decimal_places=2, null=False, default=0
    )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )


# pylint: disable=no-member
class OrderLineItem(models.Model):
    """
    The OrderLineItem model, takes in each individual product from the cart
    and iterates over the details to then pass it to the Order model.

    The order field has a foreign key relationship to the Order model, with
    a related name of lineitems.
    The product field has a foreign key relationship to the Product model.
    The quantity field is taken from wht amount submitted from within the
    cart when an order instance is created.
    lineitem_total is non editable and calculated within the save method.
    """
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')  # noqa
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)  # noqa
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)  # noqa

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem_total.
        This allows for the order total field within the Order model to
        also be updated.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns the product name and order number as a string.
        """
        return f'{self.product.name} on order {self.order.order_number}'
