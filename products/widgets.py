""" This module contains the image field widget for the product form """

from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _
# as _ is an alias for gettext_lazy, allows it to be called with '_'


class CustomClearableFileInput(ClearableFileInput):
    """
    Inherits from built in class ClearableFileInput

    Overrides the clear checkbox label,
    the initial text, the input text and the template name With custom values.

    Refer to the custom html template in the products app, for more details.
    """
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'  # noqa: E501
