""" This module tests the product app views """

from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Type, Product
from .product_form import ProductForm


class TestProductViews(TestCase):
    """
    Contains the tests for the views located in the product app in views.py.
    Focusing on the views which render all and specific products.
    """

    def setUp(self):
        """
        Creates a Product database test case.
        """
        sour = Type.objects.create(
            name='sour',
            friendly_name='Sour',
        )

        chewy = Type.objects.create(
            name='chewy',
            friendly_name='Chewy'
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

        Product.objects.create(
            type=chewy,
            name='Bon Bons',
            description='A chewy Sweet',
            popular_in_80s=False,
            popular_in_90s=False,
            popular_in_00s=True,
            weight_in_grams='75',
            price='2.99',
        )

    def test_get_products_page(self):
        """
        Tests the product page renders.

        Collects the products created in the setUp method,
        storing it in the products variable. Asserts the length of this is 2.
        Meaning all the products can be found.

        Uses Django's in-built HTTP client to get the product page URL.
        Asserts equal to status code 200, a successful HTTP response.
        """
        products = Product.objects.all()
        self.assertEqual(len(products), 2)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_get_product_detail_page(self):
        """
        Tests the product details page renders.

        Collects the first Product object created in the setUp method,
        storing it in the product variable.
        Asserts it is the object created in the method via it's
        name = Toxic Waste.

        Then Uses Django's in-built HTTP client to get the product_detail URL.
        Which is an ID value of 1, as it is the first object in the database.
        Asserts equal to status code 200, a successful HTTP response.
        """
        product = Product.objects.get(id=1)
        self.assertEqual(product.name, 'Toxic Waste')

        response = self.client.get('/products/1/')
        self.assertEqual(response.status_code, 200)

    def test_valid_search_input_returns_objects(self):
        """
        Tests the all_products view returns objects when a q value is sent.

        Uses Django's in-built HTTP client to get the query URL.
        Ensuring when the string 'toxic' is searched
        a status code 200 is returned, a successful HTTP response.
        """
        response = self.client.get('/products/?q=toxic')
        self.assertEqual(response.status_code, 200)

    def test_blank_search_input_is_handled(self):
        """
        Tests the all_products view handles a blank input q value.

        Uses Django's in-built HTTP client to get the blank query URL.
        Ensuring the correct error message is returned in the response.
        Before then ensuring the user is redirected to the all products url.
        """
        response = self.client.get('/products/?q=')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "You didn't enter any search criteria!"
        )

        self.assertRedirects(response, '/products/')

    def test_can_filter_products_by_type(self):
        """
        Tests the all_products view filters objects by type.

        Attempts to filter the Product database created in the setUp method
        by the 'sour' type. Storing it in the products variable.
        Asserts the length of this is 1.
        Meaning the database has been successfully filtered by the 'sour' type.

        Then Uses Django's in-built HTTP client to get the query URL.
        Ensuring when the type 'sour' is searched
        a status code 200 is returned, a successful HTTP response.
        """
        products = Product.objects.filter(type=1)
        self.assertEqual(len(products), 1)

        response = self.client.get('/products/?type_query=sour')
        self.assertEqual(response.status_code, 200)

    def test_can_filter_products_by_year(self):
        """
        Tests the all_products view filters objects by year.

        Filters the objects created in the setUp method by the
        years_popular fields, ensuring the length of the returned
        variable is correct as per the database.

        Then Uses Django's in-built HTTP client to get the query URL.
        Ensuring for each of the three years a status code 200 is returned.
        A successful HTTP response.
        """
        products = Product.objects.filter(popular_in_80s=True)
        self.assertEqual(len(products), 1)

        products = Product.objects.filter(popular_in_90s=True)
        self.assertEqual(len(products), 1)

        products = Product.objects.filter(popular_in_00s=True)
        self.assertEqual(len(products), 2)

        response = self.client.get('/products/?year=80')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/?year=90')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/?year=00')
        self.assertEqual(response.status_code, 200)

    def test_can_sort_products_by_name(self):
        """
        Tests the all_products view sorts objects by name.

        Uses Django's in-built HTTP client to get the sort URL's.
        Ensuring a status code 200 is returned. A successful HTTP response.
        """
        response = self.client.get('/products/?sort=name&direction=asc')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/?sort=name&direction=desc')
        self.assertEqual(response.status_code, 200)

    def test_can_sort_products_by_type(self):
        """
        Tests the all_products view sorts objects by type.

        Uses Django's in-built HTTP client to get the sort URL's.
        Ensuring a status code 200 is returned. A successful HTTP response.
        """
        response = self.client.get('/products/?sort=type&direction=asc')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/?sort=type&direction=desc')
        self.assertEqual(response.status_code, 200)

    def test_can_sort_products_by_price(self):
        """
        Tests the all_products view sorts objects by price.

        Uses Django's in-built HTTP client to get the sort URL's.
        Ensuring a status code 200 is returned. A successful HTTP response.
        """
        response = self.client.get('/products/?sort=price&direction=asc')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/?sort=price&direction=desc')
        self.assertEqual(response.status_code, 200)


class TestProductManagement(TestCase):
    """
    Contains the tests for the views located in the product app in views.py.
    Focusing on the views which allow store owners to manage products.
    """

    def setUp(self):
        """
        Initiates the Type & Product database with a single object.
        Creates a test user with admin privileges and a standard user.
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

        User.objects.create_superuser(
            username='johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@email.com',
            password='password',
        )

        User.objects.create_user(
            username='janedoe',
            first_name='Jane',
            last_name='Doe',
            email='janedoe@email.com',
            password='password',
        )

    def admin_login(self):
        """
        A helper method. Used to sign into a registered site owner.
        """

        self.client.login(
            email='johndoe@email.com',
            password='password',
        )

    def test_add_product_page_renders(self):
        """
        Tests the add_product page renders.

        Uses the admin_login method to pass superuser credentials.

        Uses Django's in-built HTTP client to get the add product page URL.
        Asserts equal to status code 200, a successful HTTP response.
        """

        self.admin_login()
        response = self.client.get('/products/add/')
        self.assertEqual(response.status_code, 200)

    def test_unregistered_users_cannot_access_add_product_page(self):
        """
        Tests an unregistered site user cannot access the add products page.

        With no user signed in, attempts to access the add products url,
        stored in the response variable.

        Uses Django's in-built HTTP client to assert the status code on
        the response variable is equal to 302, a successful HTTP redirect.
        Then asserts this redirect url is the login page.
        """

        response = self.client.get('/products/add/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/products/add/')

    def test_add_product_view_stores_object_in_database(self):
        """
        Tests a product can be added to the database through add_product view.

        Uses the admin_login method to pass superuser credentials.

        Collects the Product database made in the setUp method, asserting the
        total length of it is 1, the product added in the method.

        Instantiates an instance of the ProductForm, asserting the intended
        dict to be passed is a valid instance of the form.

        Passes the same instance as a POST request to the reverse
        of the add_product view, storing it in the response variable.
        Uses Django's in-built HTTP client to assert the status code on
        the response variable is equal to 302, a successful HTTP redirect.
        Then asserts this redirect url is the product_detail page of the
        Product object just created.

        Then collects the Product database again, asserting the
        total length of it is 2, meaning the view added the product passed
        in the form.
        """

        self.admin_login()

        products = Product.objects.all()
        self.assertEqual(len(products), 1)

        form = ProductForm(data={
            'name': 'Drumstick',
            'description': 'A chewy lollypop',
            'weight_in_grams': 10,
            'price': 1.99,
        })
        self.assertTrue(form.is_valid())

        response = self.client.post(reverse("add_product"), {
            'name': 'Drumstick',
            'description': 'A chewy lollypop',
            'weight_in_grams': 10,
            'price': 1.99,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products/2/')
        products = Product.objects.all()
        self.assertEqual(len(products), 2)

    def test_edit_product_page_renders(self):
        """
        Tests the edit_product page renders.

        Uses the admin_login method to pass superuser credentials.

        Uses Django's in-built HTTP client to get the edit product page URL
        for the product created in the setUp method.
        Asserts equal to status code 200, a successful HTTP response.
        """

        self.admin_login()
        response = self.client.get('/products/edit/1/')
        self.assertEqual(response.status_code, 200)

    def test_unregistered_users_cannot_access_edit_product_page(self):
        """
        Tests an unregistered site user cannot access the edit products page.

        With no user signed in attempts to access the edit products url for the
        product created in the setUp method, stored in the response variable.

        Uses Django's in-built HTTP client to assert the status code on
        the response variable is equal to 302, a successful HTTP redirect.
        Then asserts this redirect url is the login page.
        """

        response = self.client.get('/products/edit/1/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/accounts/login/?next=/products/edit/1/'
        )

    def test_edit_product_view_updates_object_in_database(self):
        """
        Tests a product can be updated through edit_product view.

        Uses the admin_login method to pass superuser credentials.

        Collects the Product object made in the setUp method via ID,
        asserting all the fields bar the image fields
        are equal to the values set in the method.

        Instantiates an instance of the ProductForm, asserting the intended
        dict to be passed is a valid instance of the form.

        Passes the same instance as a POST request to the reverse
        of the edit_product view with the product ID, storing it in the
        response variable. Uses Django's in-built HTTP client to assert the
        status code on the response variable is equal to 302,
        a successful HTTP redirect. Then asserts this redirect url is the
        product_detail page of the Product object just updated.

        Then collects the Product object from the database again, asserting the
        values for all the fields, bar the image fields, are now equal to the
        values passed through the edit_product url.
        """

        self.admin_login()

        product = Product.objects.get(id=1)
        self.assertEqual(product.name, 'Toxic Waste')
        self.assertEqual(product.description, 'A sour Sweet')
        self.assertEqual(product.popular_in_80s, True)
        self.assertEqual(product.popular_in_90s, True)
        self.assertEqual(product.popular_in_00s, True)
        self.assertEqual(product.weight_in_grams, 42)
        self.assertEqual(product.price, Decimal('4.99'))

        form = ProductForm(data={
            'name': 'Toxic Waste Sweets',
            'description': 'A Really Sour Sweet',
            "popular_in_80s": False,
            "popular_in_90s": False,
            "popular_in_00s": False,
            'weight_in_grams': 100,
            'price': 10.99,
        })
        self.assertTrue(form.is_valid())

        response = self.client.post(reverse("edit_product", args=[1]), {
            'name': 'Toxic Waste Sweets',
            'description': 'A Really Sour Sweet',
            "popular_in_80s": False,
            "popular_in_90s": False,
            "popular_in_00s": False,
            'weight_in_grams': 100,
            'price': 10.99,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products/1/')

        product = Product.objects.get(id=1)
        self.assertEqual(product.name, 'Toxic Waste Sweets')
        self.assertEqual(product.description, 'A Really Sour Sweet')
        self.assertEqual(product.popular_in_80s, False)
        self.assertEqual(product.popular_in_90s, False)
        self.assertEqual(product.popular_in_00s, False)
        self.assertEqual(product.weight_in_grams, 100)
        self.assertEqual(product.price, Decimal('10.99'))

    def test_unregistered_users_cannot_access_delete_product_view(self):
        """
        Tests an unregistered site user cannot access the delete products view.

        With no user signed in attempts to access the delete products url
        for the product created in the setUp method,
        stored in the response variable.

        Uses Django's in-built HTTP client to assert the status code on
        the response variable is equal to 302, a successful HTTP redirect.
        Then asserts this redirect url is the login page.
        """

        response = self.client.get('/products/delete/1/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/accounts/login/?next=/products/delete/1/'
        )

    def test_delete_product_view_removes_object_from_database(self):
        """
        Tests a product can be deleted through delete_product view.

        Uses the admin_login method to pass superuser credentials.

        Collects the Product database made in the setUp method,
        asserting the length of it is equal to 1.

        Passes the object from the database via ID to the delete_product view
        storing it in the response variable.  Uses Django's in-built HTTP
        client to assert the status code on the response variable
        is equal to 302, a successful HTTP redirect.
        Then asserts this redirect url is the all products page.

        Then collects the Product database, asserting the length is now equal
        to 0, meaning the product with an ID of 1 was deleted.
        """

        self.admin_login()

        products = Product.objects.all()
        self.assertEqual(len(products), 1)

        response = self.client.get('/products/delete/1/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products/')

        products = Product.objects.all()
        self.assertEqual(len(products), 0)

    def test_non_superusers_cant_delete_products(self):
        """
        A test to ensure authorized users cannot delete product.

        Logs into the standard user created in the setUp method,
        before collecting the Product database, asserting the length of
        it is equal to 1.

        Then passes this product to the delete product URL, stored in
        the response. Asserts the correct user feedback message is returned
        as well as a 302 status code, which redirects to the home page URL.

        The Product database is then collected again and ensured it still
        has a length of 1, meaning the product hasn't been deleted
        """

        self.client.login(
            email='janedoe@email.com',
            password='password',
        )

        products = Product.objects.all()
        self.assertEqual(len(products), 1)

        response = self.client.get('/products/delete/1/')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Sorry, only store owners can do that.'
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        products = Product.objects.all()
        self.assertEqual(len(products), 1)

    def test_non_superusers_cant_edit_products(self):
        """
        A test to ensure authorized users cannot access the edit products
        view.

        Logs into the standard user created in the setUp method,

        Then passes the product created in the setUp method to the
        edit product URL, stored in the response. Asserts the correct user
        feedback message is returned as well as a 302 status code,
        which redirects to the home page URL.
        """

        self.client.login(
            email='janedoe@email.com',
            password='password',
        )

        response = self.client.get('/products/edit/1/')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Sorry, only store owners can do that.'
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
