""" This module contains the user profile forms """

from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class NameChange(forms.ModelForm):
    """
    The form for updating the users name, rendered on name_change.html.
    """
    first_name = forms.CharField(
        label='First Name',
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Forename'}),
    )

    last_name = forms.CharField(
        label='Last Name',
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Surname'}),
    )

    class Meta:
        """
        Sets the model and fields.
        """
        model = User
        fields = ('first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        """
        Set autofocus on first_name.
        """
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['autofocus'] = True


class UserProfileForm(forms.ModelForm):
    """
    The form for saving default details, rendered on profile.html.
    """

    default_phone_number = forms.CharField(
        label='Preferred Contact Number',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Contact Number'}),
    )

    default_street_address1 = forms.CharField(
        label='First Street Address',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Street Address'}),
    )

    default_street_address2 = forms.CharField(
        label='Second Street Address',
        required=False,
    )

    default_town_or_city = forms.CharField(
        label='Town or City',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Town or City'}),
    )

    default_county = forms.CharField(
        label='County',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'County'}),
    )

    default_postcode = forms.CharField(
        label='Postal Code',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Post Code'}),
    )

    class Meta:
        """
        Sets the model.

        Set the exclude attribute and renders all fields except
        for the user field since that should never change.
        """
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Set autofocus on phone number field and labels the country field.
        """
        super().__init__(*args, **kwargs)

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        self.fields['default_country'].label = 'Country'
