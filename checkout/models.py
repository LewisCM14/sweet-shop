""" This module contains the models for the checkout app """

import uuid
from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
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

    Name, email, phone number all required. As is a full delivery address.

    The date field is auto added at the time of the order being submitted.

    Delivery cost, order total, order weight and grand total are all
    calculated using the update_total model method.

    The original cart and stripe pid fields are used to store data used
    when making comparison to ensure each Order instance is unique from
    within the webhook.

    The status field uses the STATUS tuple and allows site administrators
    to mark an orders delivery status, defaults to processing.
    """
    # Order Number
    order_number = models.CharField(max_length=32, null=False, editable=False)
    # Foreign Key to the User Model
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='orders'
    )
    # User Contact Details
    full_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=False, blank=False)
    # User Phone Number
    phone_number = models.CharField(max_length=16, null=False, blank=False)
    # User Address
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label="Country", null=False, blank=False)
    # Date of order
    date = models.DateTimeField(auto_now_add=True)
    # Calculated using model methods.
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    order_weight = models.IntegerField(null=False, default=0)

    delivery_cost = models.DecimalField(
        max_digits=4, decimal_places=2, null=False, default=0
    )

    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    # Webhook Fields
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default=''
    )
    # Order Status
    STATUS = ((0, "processing"), (1, "packaged"), (2, "posted"))
    status = models.IntegerField(choices=STATUS, default=0)

    def update_total(self):
        """
        A model method used to calculate the delivery_cost and grand_total.

        Using Sum aggregates the total sum of each line items total and weight.
        This is done by referencing each individual item created in
        the OrderLineItem model through its related name 'lineitems' and
        storing the sum of these values in order_total and order_weight.

        From here compare if the order_total is less than the
        FREE_DELIVERY_THRESHOLD located in the applications settings.

        If so delivery_cost is calculated based on order_weight. If not
        delivery_cost is set to 0 (free).

        Once delivery_cost has been calculated it is then used in
        conjunction with order_total to get the grand_total for the order.
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.order_weight = self.lineitems.aggregate(
            Sum('lineitem_weight'))['lineitem_weight__sum'] or 0

        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            if self.order_weight + 100 < 1000:
                self.delivery_cost = Decimal(2.49)
            elif self.order_weight + 100 > 1000:
                self.delivery_cost = Decimal(3.49)
        else:
            self.delivery_cost = 0

        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def _generate_order_number(self):
        """
        Generate a random, unique 32 length order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns the order number as a string.
        """
        return self.order_number


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
    lineitem_weight is non editable and calculated within the save method.
    """
    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE,
        related_name='lineitems'
    )
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False
    )
    lineitem_weight = models.IntegerField(
        null=False, blank=False, editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem_total and
        the lineitem_weight.

        This allows for the order_total and order_weight fields within the
        Order model to also be updated.
        """
        self.lineitem_total = self.product.price * self.quantity
        self.lineitem_weight = self.product.weight_in_grams * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns the product name and order number as a string.
        """
        return f'{self.product.name} on order {self.order.order_number}'
