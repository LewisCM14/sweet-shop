""" This module tests the favorites app views """

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from products.models import Type, Product
from .models import Favorites


class TestViews(TestCase):
    """
    Contains the tests for the views located in the favorites app in views.py.
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

    def add_favorite(self):
        """
        Helper Method

        Collects the user and product created in the setUp method and
        uses them to create an object in the Favorites database, The
        database is then filtered via this user and it is asserted the
        length of the result is 1 and the product is 'Raspberry Bon Bons'.

        As these assertions are imperative for the below testing
        """
        user = User.objects.get(id=1)
        product = Product.objects.get(id=1)

        Favorites.objects.create(
            product=product,
            user=user,
        )

        favorites = Favorites.objects.filter(user=user)
        self.assertEqual(len(favorites), 1)
        self.assertEqual(str(favorites[0]), 'Raspberry Bon Bons')

    def test_favorite_products_post_to_the_database(self):
        """
        Test a user can add products to their favorites.

        Uses the login helper method to pass user authentication,
        before collecting the user instance and product object
        made in the setUp method.

        Filters the Favorites database by this user and asserts
        the length of the result is 0. Then passes the product and
        user to the reverse of the favorite url. The Favorites
        database is then filtered via the user again, asserting now
        the length of the result is 1 and the string value of the
        first index is 'Raspberry Bon Bons', the product that was passed.
        """
        self.login()

        user = User.objects.get(id=1)
        product = Product.objects.get(id=1)

        favorites = Favorites.objects.filter(user=user)
        self.assertEqual(len(favorites), 0)

        self.client.get(
            reverse("favorite", args=[product.id]), {
                'product': product,
                'user': user,
            })

        favorites = Favorites.objects.filter(user=user)
        self.assertEqual(len(favorites), 1)
        self.assertEqual(str(favorites[0]), 'Raspberry Bon Bons')

    def test_check_favorite_view_redirects_to_product(self):
        """
        Test when a user favorites a product they are
        redirected back to that product.

        Uses the login helper method to pass user authentication,
        before collecting the user instance and product object
        made in the setUp method.

        Then passes the product and user to the reverse of the favorite url.
        Stored in the response variable. Then uses Django's inbuilt
        HTTP client to assert a 302 redirect code is returned and the
        reverse URL for this redirect is the product_detail URL
        with the id value of the product passed to the favorite URL.
        """
        self.login()

        user = User.objects.get(id=1)
        product = Product.objects.get(id=1)

        response = self.client.get(
            reverse("favorite", args=[product.id]), {
                'product': product,
                'user': user,
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("product_detail", args=[product.id])
        )

    def test_check_favorite_deletes_existing_product(self):
        """
        Test that when a user un-checks the favorites tab,
        an existing product is deleted.

        Calls the add_favorite helper method to create an instance
        in the Favorites database before collecting the user and
        product created in the setUp method.

        The login helper method is then called and the user and product
        passed to the reverse of the favorites url, stored is the response.

        This response variable then has it's redirected status, url and
        user feedback message asserted before the Favorites database
        is filtered via the user and the length asserted to 0.
        Meaning the existing product has been deleted.
        """
        self.add_favorite()

        user = User.objects.get(id=1)
        product = Product.objects.get(id=1)

        self.login()

        response = self.client.get(
            reverse("favorite", args=[product.id]), {
                'product': product,
                'user': user,
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("product_detail", args=[product.id])
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), f'Removed {product.name} from your favorites!'
        )

        favorites = Favorites.objects.filter(user=user)
        self.assertEqual(len(favorites), 0)

    def test_view_favorites_renders(self):
        """
        A test to check the view_favorites page renders correctly.

        Calls the add_favorite helper method to create an instance
        in the Favorites database, before calling the login method
        to pass user authentication.

        Uses Django's in-built HTTP client to get the favorites page URL.
        Asserts equal to status code 200, a successful HTTP response, then
        asserts the correct template is used before collection the
        'favorites' key from the context, asserting the Favorites DB
        instance created in the add_favorite method is returned in the context.
        """
        self.add_favorite()
        self.login()

        response = self.client.get('/favorite/my_favorites/')
        self.assertTemplateUsed(
            response, 'favorites/view_favorites.html', 'base.html'
        )

        favorites = response.context['favorites']
        self.assertEqual(len(favorites), 1)
        self.assertEqual(str(favorites[0]), 'Raspberry Bon Bons')

    def test_remove_favorite_deletes_object(self):
        """
        A test to check the remove_favorite view
        deletes the passed object from the Favorites database.

        Calls the add_favorite helper method to create an instance
        in the Favorites database before collecting the user and
        product created in the setUp method.

        The login helper method is then called and the user and product
        passed to the reverse of the remove_favorite url,
        stored is the response.

        This response variable then has it's redirected status, url and
        user feedback message asserted before the Favorites database
        is filtered via the user and the length asserted to 0.
        Meaning the existing product has been deleted.
        """
        self.add_favorite()

        user = User.objects.get(id=1)
        product = Product.objects.get(id=1)

        self.login()
        response = self.client.get(
            reverse("remove_favorite", args=[product.id]), {
                'product': product,
                'user': user,
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("my_favorites")
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), f'Removed {product.name} from your favorites!'
        )

        favorites = Favorites.objects.filter(user=user)
        self.assertEqual(len(favorites), 0)
