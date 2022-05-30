""" This module contains the user registration form """

from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from django import forms


class CustomSignupForm(SignupForm):
    """
    Extends from the allauth base signup form.

    Adds the custom sign up fields first_name and last_name.
    """

    class Meta:
        """
        Ensures the sign up form inherits from the User model and sets
        the required fields, allowing for the field_order method to be set
        """
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'email2', 'password1',
            'password2',
        )

    field_order = [
        'first_name', 'last_name', 'email', 'email2', 'password1', 'password2',
    ]

    first_name = forms.CharField(
        label='First Name',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Forename'})
    )

    last_name = forms.CharField(
        label='Last Name',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Surname'})
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
