""" This module contains the contact form for the inquiry app """

from django import forms
from .models import Inquiry


class ContactForm(forms.ModelForm):
    """
    The form to handle posting customer inquiries.
    """

    full_name = forms.CharField(
        label='Full Name',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your preferred contact name'
        }),
    )

    email = forms.EmailField(
        label='Email Address',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your preferred contact email'
        }),
    )

    phone_number = forms.CharField(
        label='Phone Number',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Preferred contact number'}),
    )

    subject = forms.CharField(
        label='Subject',
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'Attach order number if applicable'
        }),
    )

    message = forms.CharField(
        label='Your Inquiry',
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'What can we help you with?'
        }),
        max_length=200,
    )

    class Meta:
        """
        Specifies the Inquiry model to inherit from and the fields to
        display.
        """
        model = Inquiry
        fields = (
            'full_name', 'subject', 'email', 'phone_number', 'message',
        )
