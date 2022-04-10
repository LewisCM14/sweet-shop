""" This module contains the model for user profiles """

from django.db import models
from django.contrib.auth.models import User

from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history

    The user field specifies that each user can only have one profile.
    And each profile can only be attached to one user.

    The other fields in this model are the delivery information fields.
    The user is able to provide defaults for these.
    all these fields are optional.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    deafault_forname = models.CharField(max_length=20, null=True, blank=True)
    default_surname = models.CharField(max_length=20, null=True, blank=True)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)  # noqa
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)  # noqa
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)  # noqa
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)  # noqa
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True)  # noqa

    # pylint: disable=no-member
    def __str__(self):
        return self.user.username
