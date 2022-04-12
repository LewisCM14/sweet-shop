""" This module contains the models for the products app """

from django.db import models


class Type(models.Model):
    """
    A Model to give the prodcuts a type.
    """
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        """
        Inbuilt method to adjust name in admin panel.
        """
        verbose_name_plural = "Type"

    # pylint: disable=invalid-str-returned
    def __str__(self):
        """
        Returns the specific category name as a string.
        """
        return self.name

    def get_friendly_name(self):
        """
        A model method to return the friendly name.
        """
        return self.friendly_name


class Product(models.Model):
    """
    A Model to hold the product info.

    category field is a forign key to the Type Model above.
    Each product requires a name, description, year and price.
    Everything else is optional.
    """

    # A tuple to hold the key for the year field.
    YEAR = ((0, "90s & 00s"), (1, "90s"), (2, "00s"))

    type = models.ForeignKey(
        'Type', null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=254)
    description = models.TextField()
    year = models.IntegerField(choices=YEAR, default=0)
    has_weights = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    # pylint: disable=invalid-str-returned
    def __str__(self):
        """
        Returns the specific product name as a string.
        """
        return self.name
