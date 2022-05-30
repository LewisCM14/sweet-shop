""" This module contains the models for the inquiry app """

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Inquiry(models.Model):
    """
    A model to store customer inquiries.

    Collects the User ID if submitted by a authorized user, allowed
    to be blank if not.

    Requires full_name, email, phone, subject and inquiry message
    from user to allow submission, attaches date sent
    upon submission for ordering within admin.
    """
    # User
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    # Contact Details
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phoneNumberRegex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone_number = models.CharField(
        validators=[phoneNumberRegex], max_length=16,)
    # Inquiry
    subject = models.CharField(max_length=30)
    message = models.TextField(max_length=200)
    # Date Sent
    date = models.DateField(auto_now_add=True)

    class Meta:
        """
        Class meta, sets the verbose name in the admin panel.
        """
        verbose_name_plural = "Inquiries"

    def __str__(self):
        """
        Returns the string value of the name & date of the inquiry.
        """
        return f'{self.full_name} opened {self.subject } on {self.date}'
