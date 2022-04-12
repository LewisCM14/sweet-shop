""" This module contains the models for the products app """

from django.db import models


class Category(models.Model):
    """
    A Model to give the prodcuts a category.
    """
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        """
        Inbuilt method to adjust name in admin panel.
        """
        verbose_name_plural = "Categories"

    # pylint: disable=invalid-str-returned
    def __str__(self):
        """
        Returns the category name as a string.
        """
        return self.name

    def get_friendly_name(self):
        """
        A model method to return the friendly name.
        """
        return self.friendly_name
