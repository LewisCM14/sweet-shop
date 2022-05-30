""" This module contains the models for the review app """

from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class Reviews(models.Model):
    """
    A model to store the product reviews.

    Collects the user from the User model and the product they
    have chosen to review from the Product model,
    if either the User or the product is deleted,
    the database entry is removed.

    The rating field uses the RATING tuple to store the score out of
    5 for the product, defaulting to choice 4, or 5 starts
    and the review field holds the text specific to the review.

    Also stores the date the user created the review,
    for use in the admin/display logic.
    """
    # User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Rating
    RATING = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"))
    rating = models.IntegerField(choices=RATING, default=5)
    # Review
    review = models.TextField(max_length=200)
    # Date Added
    added_on = models.DateField(auto_now_add=True)

    class Meta:
        """
        Class meta, sets the verbose name in the admin panel
        and ensures each user can only have one review per product.
        """
        verbose_name_plural = "Reviews"
        unique_together = [['user', 'product']]

    def __str__(self):
        """
        Returns the string value for the products name.
        """
        return f'{self.product.name} rated {self.rating} stars'
