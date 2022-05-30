""" This module tests the checkout app views """

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from products.models import Type, Product
from profiles.models import UserProfile
from .models import Order, OrderLineItem


class TestViews(TestCase):
    """
    Contains the tests for the views located in the checkout app in views.py.
    """

    def setUp(self):
        """
        Creates a User test case before
        initiating the Product database with an object for testing.
        """
        User.objects.create_user(
            username='Test User',
            first_name='John',
            last_name='Doe',
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

    def test_checkout_page_redirects_if_cart_empty(self):
        """
        Tests the checkout page redirects to the product page if
        the cart is empty.

        Uses Django's in-built HTTP client to get the checkout page URL.
        Storing it in the response variable. Then asserts the status code
        on this is equal to a 302 redirect response.
        Then using Django's get_messages method asserts a error message
        with the desired string value is returned to the user before asserting
        the redirect URL is the products page.
        """

        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "There's nothing in your cart at the moment"
        )
        self.assertRedirects(response, '/products/')

    def test_checkout_page_renders(self):
        """
        Tests the checkout page renders.

        Initiates a cart instance in the session with the initiate_cart
        helper method.

        Uses Django's in-built HTTP client to get the checkout page URL.
        Storing it in the response variable. Then asserts the status code
        on this is equal to a 200, a successful HTTP response.
        """

        self.initiate_cart()
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)

    def test_order_posts_to_the_database(self):
        """
        Test the checkout view posts valid OrderForms to the database.

        Initiates a cart instance in the session with the initiate_cart
        helper method and collects the product object created in the setUp
        method for use in making assertions.

        Posts a valid OrderForm instance to the checkout URL, storing it
        in the response variable, then uses Django's inbuilt HTTP client to
        assert its status code is equal to a 302 redirect response.

        Then collects the created Order and OrderLineItem objects via ID.
        Asserting the value for each field in the Order object is equal to the
        passed values in the POST response. Before asserting the ForeignKey
        'order' field on the OrderLineItem model is the corresponding order,
        the 'product' field is equal to the product created in the setUp method
        and then passed to the cart instance and the quantity, total and price
        fields have the correct values.

        Then asserts the user is directed to the correct checkout success URL.
        """
        self.initiate_cart()
        product = Product.objects.get(id=1)

        response = self.client.post(
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
        self.assertEqual(response.status_code, 302)

        order = Order.objects.get(id=1)
        self.assertEqual((order.full_name), 'John Doe')
        self.assertEqual((order.email), 'johndoe@email.com')
        self.assertEqual((order.phone_number), '11111111111')
        self.assertEqual((order.street_address1), '4 privet drive')
        self.assertEqual((order.street_address2), '')
        self.assertEqual((order.town_or_city), 'little whinging')
        self.assertEqual((order.county), 'surrey')
        self.assertEqual((order.postcode), 'CR2 5ER')
        self.assertEqual((order.country), 'GB')

        line_item = OrderLineItem.objects.get(id=1)
        self.assertEqual((line_item.order), order)
        self.assertEqual((line_item.product), product)
        self.assertEqual((line_item.quantity), 1)
        self.assertEqual((line_item.lineitem_total), Decimal('1.99'))
        self.assertEqual((line_item.lineitem_weight), 200)

        self.assertRedirects(
            response, reverse("checkout_success", args=[order.order_number])
        )

    def test_checkout_success_page_deletes_the_cart(self):
        """
        Tests the checkout success page deletes the cart from the session.

        Initiates a cart instance in the session with the initiate_cart
        helper method.

        Posts a valid OrderForm instance to the checkout URL, storing it
        in the response variable, then uses Django's inbuilt HTTP client to
        assert its status code is equal to a 302 redirect response, then
        asserts the user is redirected to the checkout_success page for this
        specific order, along with receiving a feedback message.

        Then collects the session and asserts the 'cart' key is no longer
        in it.
        """

        self.initiate_cart()

        response = self.client.post(
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
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertRedirects(
            response, reverse("checkout_success", args=[order.order_number])
        )

        session = self.client.session
        self.assertNotIn('cart', session)

    def test_order_saves_to_user_profile(self):
        """
        A test to ensure successful Orders are saved against the users profile

        Uses the login helper method to pass user authentication,
        Then confirms the user created in the setUp method has a
        UserProfile via the ID field on the profile variable.

        The initiate_cart helper method is then called and a order
        instance passed to the checkout view. This order is then collected
        and asserted there is currently no UserProfile attached.
        This same order instance is then passed to the checkout_success URL
        before having the user_profile field checked again to assert it now
        has profile of the signed in user created within the setUp method
        attached to it.
        """
        self.login()

        profile = UserProfile.objects.get(id=1)
        self.assertEqual(profile.user.username, 'Test User')

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
        self.assertEqual(order.user_profile, None)

        self.client.post(
            reverse("checkout_success", args=[order.order_number])
        )

        order = Order.objects.get(id=1)
        self.assertEqual(order.user_profile, profile)
