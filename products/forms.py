""" This module contains the product form used by store managers """

from django import forms
from .models import Product, Type


# pylint: disable=no-member
class ProductForm(forms.ModelForm):
    """
    Extends from the base model form.
    """

    class Meta:
        """
        Defines model used and fields required.
        """
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Override the init method to make changes to the fields,
        allowing Types to show up in the form using their friendly name.

        First collect all the 'Types. Then create a list of tuples
        of the friendly names associated with the IDs.
        Use the friendly names, to update the type field on the form
        to use those for choices instead of using the ID.
        """
        super().__init__(*args, **kwargs)
        types = Type.objects.all()
        friendly_names = [(t.id, t.get_friendly_name()) for t in types]

        self.fields['type'].choices = friendly_names
