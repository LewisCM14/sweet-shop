""" This module contains the models for the favorites app """

from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class Favorites(models.Model):
    """
    A model to store a users favorites products.

    Collects the user from the User model and the products they
    have added to their favorites from the Product model,
    if either the User or the product is deleted,
    the database entry is removed.

    Also stores the date the user added the product to their favorites,
    for use in the admin logic.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Class meta, sets the verbose name in the admin panel
        and ensures each user can only favorite each product once.
        """
        verbose_name_plural = "Favorites"
        unique_together = [['user', 'product']]

    def __str__(self):
        """
        Returns the string value for the products name.
        """
        return self.product.name
