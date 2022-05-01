""" This module contains the model for user profiles """

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    default_forname = models.CharField(max_length=20, null=True, blank=True)
    default_surname = models.CharField(max_length=20, null=True, blank=True)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)  # noqa: E501
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)  # noqa: E501
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)  # noqa: E501
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)  # noqa: E501
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True)  # noqa: E501

    # pylint: disable=no-member
    def __str__(self):
        """
        Returns the username of the user instance as a string
        """
        return self.user.username


# pylint: disable=no-member
# pylint: disable=unused-argument
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the UserProfile.

    Receiver for the post save event from the user model.
    Each time a user object is saved, either create a profile for them,
    if the user has just been created,
    Or just save the profile to update it if the user already existed.
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
