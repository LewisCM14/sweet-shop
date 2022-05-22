""" This module contains the post review form for the review app """

from django import forms
from .models import Reviews


class PostReviewForm(forms.ModelForm):
    """
    The form to handle posting product reviews.
    """

    RATING = ((5, "5 Stars"), (4, "4 Stars"), (3, "3 Stars"), (2, "2 Stars"), (1, "1 Star"))  # noqa: E501

    rating = forms.ChoiceField(
        label='Rating',
        required=True,
        choices=RATING,
        widget=forms.Select,
    )

    review = forms.CharField(
        label='Review',
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'What did you think of the product?'
        }),
        max_length=200,
    )

    class Meta:
        """
        Specifies the  Reviews model to inherit from and the fields to
        display.
        """
        model = Reviews
        fields = ('rating', 'review',)
