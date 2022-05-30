""" This module handles the views for the inquiry app """

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from profiles.models import UserProfile
from .contact_form import ContactForm


def send_notification_email(inquiry):
    """
    A function to handle sending inquiry confirmation emails.

    Collects the customers email from the passed in inquiry.
    Then render_to_string the files located within the inquiry templates
    notification_emails folder, passing in the inquiry as context.

    The Django send_mail function is then called with the email subject,
    body, delivery email and the recipients email.
    """
    customer_email = inquiry.email
    subject = render_to_string(
        'inquiry/notification_emails/notification_email_subject.txt',
        {'inquiry': inquiry})
    body = render_to_string(
        'inquiry/notification_emails/notification_email_body.txt',
        {'inquiry': inquiry, 'contact_email': settings.DEFAULT_FROM_EMAIL})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [customer_email]
    )


def contact_us(request):
    """
    Renders the contact_us.html template in the browser.

    Handles pre-filling sections of the OrderForm by
    collecting the users full name and email if they are
    authenticated, and if they have a UserProfile collecting their
    default phone number. Returns a blank form of none of this information
    is stored.

    On the POST request collects the form data and passes it to the
    ContactFrom, if invalid the form is returned to the user with the errors
    displayed. If valid, the instance is saved without committing and the
    users authentication status is checked, if the request was made by an
    authorized user their ID is attached to the inquiry before it is
    posted to the database. If not the form is posted with that field blank.

    Once a valid inquiry has been posted to the database the above
    send_notification_email function is called in order to send an email
    detailing the inquiry they have made to the user.
    """
    user = request.user

    if user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=user)
            contact_form = ContactForm(initial={
                'full_name': user.get_full_name(),
                'email': profile.user.email,
                'phone_number': profile.default_phone_number,
            })
        except UserProfile.DoesNotExist:
            contact_form = ContactForm()
    else:
        contact_form = ContactForm()

    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'subject': request.POST['subject'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'message': request.POST['message'],
        }
        contact_form = ContactForm(form_data)
        if contact_form.is_valid():
            inquiry = contact_form.save(commit=False)
            if user.is_authenticated:
                inquiry.user = request.user
                inquiry.save()
                send_notification_email(inquiry)
            else:
                inquiry.save()
                send_notification_email(inquiry)

            messages.info(request, 'Your inquiry has been sent. \
                We will be in touch as soon as possible.')
            return redirect(reverse('mail_success'))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check the information you provided.')

    template = 'inquiry/contact_us.html'

    context = {
        'contact_form': contact_form,
    }

    return render(request, template, context)


def mail_success(request):
    """ A view to render the main success template """
    return render(request, 'inquiry/mail_success.html')
