""" This module contains the models for the products app """

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Type(models.Model):
    """
    A Model to give the products a type.
    """
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        """
        Inbuilt method to adjust name in admin panel.
        """
        verbose_name_plural = "Type"

    def __str__(self):
        """
        Returns the specific category name as a string.
        """
        return f'{self.name}'

    def get_friendly_name(self):
        """
        A model method to return the friendly name.
        """
        return self.friendly_name


class Product(models.Model):
    """
    A Model to hold the product info.

    type field is a foreign key to the Type Model above.

    Each product requires a name, description, weight and price.

    The years_popular fields are then optional.
    These boolean check boxes allow the site owner
    to dictate filtering by year within the store.

    The image fields are then also optional. if no image is provided
    this is handled within the app settings/root media folder.
    """

    # Foreign Key's
    type = models.ForeignKey(
        'Type', null=True, blank=True, on_delete=models.SET_NULL
    )
    # Name & Description
    name = models.CharField(max_length=254)
    description = models.TextField()
    # Years Popular
    popular_in_80s = models.BooleanField()
    popular_in_90s = models.BooleanField()
    popular_in_00s = models.BooleanField()
    # Weight & Price
    weight_in_grams = models.IntegerField(validators=[MaxValueValidator(1000)])
    price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    # Image Fields
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        """
        Returns the specific product name as a string.
        """
        return f'{self.name}'
