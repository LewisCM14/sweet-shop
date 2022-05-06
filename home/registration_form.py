""" This module contains the user registration form """

from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from django import forms


class CustomSignupForm(SignupForm):
    """
    Extends from the allauth base signup form.

    Adds the custom sign up fields forname and surname.
    """

    class Meta:
        """
        Ensures the sign up form inherits from the User model and sets
        the required fields, allowing for the field_order method to be set
        """
        model = User
        fields = ('forname', 'surname', 'email1', 'email2', 'password1', 'password2',)  # noqa: E501

    field_order = ['forname', 'surname', 'email1', 'email2', 'password1', 'password2', ]  # noqa: E501

    forname = forms.CharField(
        label='Forname',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )

    surname = forms.CharField(
        label='Surname',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.forname = self.cleaned_data['forname']
        user.surname = self.cleaned_data['surname']
        user.save()
        return user
