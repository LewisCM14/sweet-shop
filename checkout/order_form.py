""" This module contains the order form for the checkout app """

from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    The order form.
    """

    full_name = forms.CharField(
        label='Full Name',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'}),
    )

    email = forms.EmailField(
        label='Email Address',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Email Address'}),
    )

    phone_number = forms.CharField(
        label='Phone Number',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Preferred Contact Number'}),  # noqa: E501
    )

    street_address1 = forms.CharField(
        label='First Street Address',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Street Address'}),
    )

    street_address2 = forms.CharField(
        label='Second Street Address',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Street Address'}),
    )

    town_or_city = forms.CharField(
        label='Town or City',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Town or City'}),
    )

    county = forms.CharField(
        label='County',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'County'}),
    )

    postcode = forms.CharField(
        label='Postal Code',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Post Code'}),
    )

    class Meta:
        """
        Specifies the  Order model to inherit from and the fields to
        display, excludes all autogenerated fields.
        """
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'county',
                  'country',)

    def __init__(self, *args, **kwargs):
        """
        Over ride the default save method.

        Add the autofocus class to the 'full_name' field.
        """
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['autofocus'] = True
