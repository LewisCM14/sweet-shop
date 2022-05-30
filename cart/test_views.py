""" This module tests the cart app views """

from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from products.models import Type, Product


class TestView(TestCase):
    """
    Contains the tests for the views located in the cart app in views.py.
    """
    def setUp(self):
        """
        Creates a Product database test case.
        """
        sour = Type.objects.create(
            name='sour',
            friendly_name='Sour',
        )

        Product.objects.create(
            type=sour,
            name='Toxic Waste',
            description='A sour Sweet',
            popular_in_80s=True,
            popular_in_90s=True,
            popular_in_00s=True,
            weight_in_grams='42',
            price='4.99',
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

    def test_cart_view_renders(self):
        """
        Tests the view_cart page renders.

        Uses Django's in-built HTTP client to get the product page URL.
        Asserts equal to status code 200, a successful HTTP response.
        """

        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_redirects_to_item(self):
        """
        Tests the add_to_cart view redirects back to the product_detail
        page of the product added.

        Passes the ID for the product created in the setUp method as the
        argument to the reverse of the add_to_cart url,
        with a quantity of 1 and redirect_url value for that of the product.

        Uses Django's in-built HTTP client to asserts the status code is
        equal to 302, a successful HTTP redirect response. Before asserting the
        redirect url is the correct one for the object added.
        """

        response = self.client.post(reverse("add_to_cart", args=[1]), {
            'quantity': '1',
            'redirect_url': '/products/1/',
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products/1/')

    def test_cart_stores_and_updates_product_plus_quantity(self):
        """
        Tests the add_to_cart view stores and updates
        the passed product and its quantity.

        Collects the Product object created in the setUp method, storing it
        in the product variable. Initiates a quantity variable with a value
        of 1. Passes these to the reverse of the add_to_cart url,
        with a redirect_url value for that of the product.

        Then collects the created session,
        storing it in the 'session' variable. From this variable
        asserts the 'cart' key has a length of 1.
        Meaning a cart object has been created and a key:value pair passed.

        From the session variable then collects the cart dict itself,
        storing it in the cart variable. From here asserts that the
        value of the key '1' is the integer 1. Meaning the product with an ID
        of '1' has a quantity of 1 stored within the cart dict.

        Then Passes the ID for the product created in the setUp method as the
        argument to the reverse of the add_to_cart url again,
        with a new quantity of 2.

        Collection the cart dict itself from the session again,
        asserting that the new value for key '1' is 3.
        The sum of the two quantity variables crated within the test case.
        Meaning the add_to_cart view stores and updates the key:value pairs
        of the passed products.
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

        quantity = 2

        self.client.post(reverse("add_to_cart", args=[product.id]), {
            'quantity': quantity,
            'redirect_url': '/products/1/',
        })

        session = self.client.session
        cart = session['cart']
        self.assertEqual(cart.get('1'), 3)

    def test_item_quantity_updates_within_cart(self):
        """
        Tests the product quantity can be updated within cart.html.

        Runs the initiate_cart helper method.

        Collects the Product object created in the setUp method, storing it
        in the product variable. Initiates a quantity variable with a value
        of 2. Passes these to the reverse of the adjust_cart url, stored in
        the response variable.

        Uses Django's in-built HTTP client to asserts the status code for the
        response variable is equal to 302, a successful HTTP redirect response.
        Before asserting the redirect url that of cart.html.

        Collects the cart dict from the session,
        asserting that the new value for key '1' is 2.
        The value of the quantity variables passed to it.
        Meaning the adjust_cart view updated the key:value pair
        of the passed product.
        """
        self.initiate_cart()

        product = Product.objects.get(id=1)
        quantity = 2

        response = self.client.post(
            reverse("adjust_cart", args=[product.id]), {
                'quantity': quantity,
            })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cart/')

        session = self.client.session
        cart = session['cart']
        self.assertEqual(cart.get('1'), 2)

    def test_item_with_quantity_0_is_removed_from_cart(self):
        """
        Tests an item updated with a quantity of 0, is removed from the cart.

        Runs the initiate_cart helper method.

        Collects the Product object created in the setUp method, storing it
        in the product variable. Initiates a quantity variable with a value
        of 0. Passes these to the reverse of the adjust_cart url, stored in
        the response variable.

        Uses Django's in-built HTTP client to asserts the status code for the
        response variable is equal to 302, a successful HTTP redirect response.
        Before asserting the redirect url that of cart.html.

        Collects the cart dict from the session,
        asserting the value of 1 for the key '1' is now false. Before then
        asserting that the new value for key '1' is None.
        Meaning that not only was the quantity set to 0, the key:pair itself
        was removed from the cart dict.
        """
        self.initiate_cart()

        product = Product.objects.get(id=1)
        quantity = 0

        response = self.client.post(
            reverse("adjust_cart", args=[product.id]), {
                'quantity': quantity,
            })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cart/')

        session = self.client.session
        cart = session['cart']
        self.assertFalse(cart.get('1'), 1)
        self.assertEqual(cart.get('1'), None)

    def test_item_can_be_removed_from_cart(self):
        """
        Tests an item can be removed from the cart.

        Runs the initiate_cart helper method.

        Collects the Product object created in the setUp method, storing it
        in the product variable. Then passes these to the reverse of
        the remove_from_cart url.

        Collects the cart dict itself from the session,
        asserting the value of 1 for the key '1' is now false. Before then
        asserting that the new value for key '1' is None.
        Meaning that the product was removed from the cart dict.
        """
        self.initiate_cart()

        product = Product.objects.get(id=1)

        self.client.post(reverse("remove_from_cart", args=[product.id]))

        session = self.client.session
        cart = session['cart']
        self.assertFalse(cart.get('1'), 1)
        self.assertEqual(cart.get('1'), None)

    def test_add_item_limit_in_cart_is_25(self):
        """
        A test to ensure the add_to_cart view cannot add more than 25 of
        a specific item.

        Collects the product created in the setUp method and sets the quantity
        to 25, passing these two values to the reverse of the add_to_cart view,
        before collecting the cart from the session and ensuring
        it has a len of 1 and the value of this key is 25.

        Another post is made to the add_to_cart view again, this time stored
        in the response, with a specific quantity of 1, it is then asserted
        that this response redirects correctly and the two user feedback
        messages stored within the session have the correct str value, before
        the cart is collected again and it is asserted the quantity
        remains at 25. Meaning it has a limit of 25 because the 1 wasn't added.
        """
        product = Product.objects.get(id=1)
        quantity = 25

        self.client.post(reverse("add_to_cart", args=[product.id]), {
            'quantity': quantity,
            'redirect_url': '/products/1/',
        })

        session = self.client.session
        self.assertEqual(len(session['cart']), 1)

        cart = session['cart']
        self.assertEqual(cart.get('1'), quantity)

        response = self.client.post(reverse(
            "add_to_cart", args=[product.id]), {
                'quantity': 1,
                'redirect_url': '/products/1/',
            })

        self.assertRedirects(response, '/products/1/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(
            str(messages[0]), f'Added {product.name} to your cart'
        )
        self.assertEqual(
            str(messages[1]), f'The total weight of {product.name} would now exceed 5kg, Please contact us directly to arrange purchase of individual items exceeding 5kg.'  # noqa: E501
        )

        cart = session['cart']
        self.assertEqual(cart.get('1'), 25)

    def test_update_item_limit_in_cart_is_25(self):
        """
        A test to ensure the adjust_cart view cannot add more than 25 of
        a specific item.

        Calls the initiate_cart helper method before collecting the product
        created in the setUp method passes this with a quantity of 26,
        to the reverse of the adjust_cart view, storing it in the response
        variable. It is then asserted that this response redirects
        correctly and the error message stored within the session
        has the correct str value, before the cart is collected again
        and it is asserted the quantity remains at 1.

        The product with a quantity of 25 is then passed to the reverse of the
        adjust_cart view. storing it in the response variable.
        It is then asserted that this response redirects correctly before
        the cart is collected again and it is asserted the quantity
        is now 25, meaning it has a limit of 25.
        """
        self.initiate_cart()

        product = Product.objects.get(id=1)

        response = self.client.post(reverse(
            "adjust_cart", args=[product.id]), {
                'quantity': 26,
                'redirect_url': '/products/1/',
            })
        self.assertRedirects(response, (reverse('view_cart')))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), f'The total weight of {product.name} would now exceed 5kg, Please contact us directly to arrange purchase of individual items exceeding 5kg.')  # noqa: E501

        session = self.client.session
        self.assertEqual(len(session['cart']), 1)
        cart = session['cart']
        self.assertEqual(cart.get('1'), 1)

        response = self.client.post(reverse(
            "adjust_cart", args=[product.id]), {
                'quantity': 25,
                'redirect_url': '/products/1/',
            })
        self.assertRedirects(response, (reverse('view_cart')))

        session = self.client.session
        self.assertEqual(len(session['cart']), 1)
        cart = session['cart']
        self.assertEqual(cart.get('1'), 25)
