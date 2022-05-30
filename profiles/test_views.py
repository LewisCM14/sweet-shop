""" This module tests the profile app views """

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from products.models import Type, Product
from checkout.models import Order
from .models import UserProfile


class TestView(TestCase):
    """
    Contains the tests for the views.
    Located in the profile app in views.py.
    """

    def setUp(self):
        """
        Creates a User test case and an instance of the Product database.
        """
        User.objects.create_user(
            username='Test User',
            first_name='john',
            last_name='doe',
            email='johndoe@email.com',
            password='password',
        )

        chewy = Type.objects.create(
            name='chewy_sweets',
            friendly_name='Chewy Sweets',
        )

        Product.objects.create(
            type=chewy,
            name='Raspberry Bon Bons',
            description='A Chewy Sweet',
            popular_in_80s=False,
            popular_in_90s=True,
            popular_in_00s=True,
            weight_in_grams=200,
            price=Decimal(1.99),
        )

    def login(self):
        """
        Helper Method

        Logs into the User created in the setUp method.
        Called in the below tests to pass user authentication conditions.
        """
        self.client.login(
            email="johndoe@email.com",
            password='password',
        )

    def initiate_cart(self):
        """
        A helper method to initiate an instance of the cart object.
        Then stored within the session, used to then perform tests on.

        Then collects the created session,
        storing it in the 'session' variable. From this variable
        asserts the 'cart' key has a length of 1.
        Meaning a cart object has been created and a key:value pair passed.

        From the session variable then collects the cart dict itself,
        storing it in the cart variable. From here asserts that the
        value of the key '1' is the integer 1. Meaning the product with an ID
        of '1' has a quantity of 1 stored within the cart dict.

        These tests are done as it is imperative the method creates a cart
        object within the session, and the key:value pair in it is pre-defined.
        """

        product = Product.objects.get(id=1)
        quantity = 1

        self.client.post(reverse("add_to_cart", args=[product.id]), {
            'quantity': quantity,
            'redirect_url': '/products/1/',
        })

        session = self.client.session
        self.assertEqual(len(session['cart']), 1)

        cart = session['cart']
        self.assertEqual(cart.get('1'), quantity)

    def test_get_profile_page(self):
        """
        Tests the profile page renders.

        Uses the login helper method to sign into the test case User.
        Passing the views authentication conditions.
        Uses Django's in-built HTTP client to get the profile page URL.
        Asserts equal to status code 200, a successful HTTP response.
        """
        self.login()
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_user_profile_form_saves(self):
        """
        Tests a valid UserProfileForm instance posts to the database.

        Uses the login helper method to sign into the test case User.
        Passing the views authentication conditions.

        Collects the profile for the user via ID storing it in user_profile,
        then asserts all the fields in this model currently have no value set/

        Posts a valid UserProfileForm instance to the reverse of
        the profile URL. Then uses Django's in-built HTTP client to ensure
        it returns a successful HTTP 200 response.

        Then collects the profile for the user via ID again,
        asserting all the fields in this model now have values equal to the
        data passed in the POST request.
        """
        self.login()
        user_profile = UserProfile.objects.get(id=1)

        self.assertEqual(user_profile.default_phone_number, None)
        self.assertEqual(user_profile.default_street_address1, None)
        self.assertEqual(user_profile.default_street_address2, None)
        self.assertEqual(user_profile.default_town_or_city, None)
        self.assertEqual(user_profile.default_county, None)
        self.assertEqual(user_profile.default_postcode, None)
        self.assertEqual(user_profile.default_country, None)

        response = self.client.post(
            reverse("profile"), {
                'default_phone_number': '11111111111',
                'default_street_address1': '4 privet drive',
                'default_street_address2': '',
                'default_town_or_city': 'little whinging',
                'default_county': 'surrey',
                'default_postcode': 'CR2 5ER',
                'default_country': 'GB',
            })
        self.assertEqual(response.status_code, 200)

        user_profile = UserProfile.objects.get(id=1)

        self.assertEqual(user_profile.default_phone_number, '11111111111')
        self.assertEqual(
            user_profile.default_street_address1, '4 privet drive'
        )
        self.assertEqual(user_profile.default_street_address2, '')
        self.assertEqual(user_profile.default_town_or_city, 'little whinging')
        self.assertEqual(user_profile.default_county, 'surrey')
        self.assertEqual(user_profile.default_postcode, 'CR2 5ER')
        self.assertEqual(user_profile.default_country, 'GB')

    def test_order_history_is_collected(self):
        """
        A test to confirm a users order history is collected in the view.

        Using the class helper methods, logs into the test user and
        initiates a cart, posting this cart instance to the checkout
        view and then using the created order to post to the
        checkout_success view in order to attach it to the test users
        profile.

        This profile is then collected via its ID and the all method is
        used to collect any orders saved to their profile, this variables
        is asserted to equal 1, before the order_number is used to post
        to the order_history URL and Django's inbuilt HTTP client is used
        to confirm a status code 200 is received.
        """
        self.login()
        self.initiate_cart()
        self.client.post(
            reverse("checkout"), {
                'full_name': 'John Doe',
                'email': 'johndoe@email.com',
                'phone_number': '11111111111',
                'street_address1': '4 privet drive',
                'street_address2': '',
                'town_or_city': 'little whinging',
                'county': 'surrey',
                'postcode': 'CR2 5ER',
                'country': 'GB',
                'client_secret': 'client secret test string',
            })
        order = Order.objects.get(id=1)
        self.client.post(
            reverse("checkout_success", args=[order.order_number])
        )

        profile = UserProfile.objects.get(id=1)
        orders = profile.orders.all()
        self.assertEqual(len(orders), 1)

        response = self.client.get(
            reverse('order_history', args=[order.order_number])
        )
        self.assertEqual(response.status_code, 200)

    def test_users_can_change_name(self):
        """
        A test to confirm users can change their first & last name.

        Uses the login helper method to pass user authentication
        before collecting the user via their ID and confirming the
        values for their first & last name.

        A POST request is then made to the change_name URL,
        stored in the response variable, with updated values for
        the first_name and last_name fields. Django's HTTP client
        is then used to confirm a status code 200 was returned.
        before the user is collected again and it is asserted the name
        fields have been updated to the values given to the change_name view.
        """
        self.login()

        user = User.objects.get(id=1)
        self.assertEqual(user.first_name, 'john')
        self.assertEqual(user.last_name, 'doe')

        response = self.client.post(reverse("change_name"), {
            'first_name': 'John',
            'last_name': 'Doe',
        })
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(id=1)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')

    def test_invalid_name_changes_dont_save(self):
        """
        A test to confirm invalid name changes don't update the name fields.

        Uses the login helper method to pass user authentication
        before collecting the user via their ID and confirming the
        values for their first & last name.

        A POST request is then made to the change_name URL,
        stored in the response variable, with invalid values for
        the first_name and last_name fields. Django's get_messages
        method is then used to confirm an error was returned,
        with the desired string. Before the user is collected again
        and it is asserted the name fields haven't been altered.
        """
        self.login()

        user = User.objects.get(id=1)
        self.assertEqual(user.first_name, 'john')
        self.assertEqual(user.last_name, 'doe')

        response = self.client.post(reverse("change_name"), {
            'first_name': '',
            'last_name': '',
        })

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "Update failed. Please ensure the form is valid."
        )

        user = User.objects.get(id=1)
        self.assertEqual(user.first_name, 'john')
        self.assertEqual(user.last_name, 'doe')
