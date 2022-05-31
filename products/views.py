""" This module handles the views for the products app """

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from review.models import Reviews
from review.review_form import PostReviewForm
from favorites.models import Favorites

from .models import Product, Type
from .product_form import ProductForm


def all_products(request):
    """
    A view to show all products

    Search Functionality:
    Handles the search function in the main nav.
    Takes in the GET request from the form,
    storing the input named as 'q' in the query variable.
    If no value is input, an error message is returned
    and the user is redirected to the products url.
    If there is a value input, the queries variable is set
    equal to a Q object, where the name or the description,
    contains the query (case insensitive).
    The products variable is then filtered by the queries variable.

    Type Filtering:
    Takes in the type_query from the GET request,
    storing the required type value in the type_filter variable.
    Then filters the products returned in the view by the name value
    of the type_filter. Then converts the list of strings of type names
    passed through the URL into a list of actual type objects,
    so that all their fields can be accessed in the template.

    Year Filtering:
    Filtering by year takes in the GET request, then uses an if/else
    statement to filter products by the years_popular fields, based on
    the value given in the request.

    Product Sorting:
    Takes in the sort criteria from the GET request.
    Storing it in the sortkey variable for use in the function,
    whilst also preserving the original sort criteria in a variable
    for use in the template.

    Then checks if direction was in the GET request.
    Pre-pending a minus to the sortkey variable if the direction was
    equal to descending (desc) Before ordering the products by the
    final sortkey variable.
    """
    products = Product.objects.all()
    # Set to none initially to ensure no error is returned in context
    query = None
    type_filter = None
    year = None
    sort = None
    direction = None

    if request.GET:
        if 'year' in request.GET:
            year = request.GET['year']
            if year == '80':
                products = Product.objects.filter(popular_in_80s=True)
            elif year == '90':
                products = Product.objects.filter(popular_in_90s=True)
            elif year == '00':
                products = Product.objects.filter(popular_in_00s=True)

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'type':
                sortkey = 'type__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'type_query' in request.GET:
            type_filter = request.GET['type_query'].split(',')
            products = products.filter(type__name__in=type_filter)
            type_filter = Type.objects.filter(name__in=type_filter)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!"
                )
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)  # noqa: E501
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'year': year,
        'current_type': type_filter,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    A view to show individual product details.

    Collects the product from the database to return as context.
    Also collects the PostReviewForm to return as context.

    Uses the collected product to filter the Review database
    and return all reviews for it back as context.

    Collects the user, and if authenticated filters the Favorites
    database by user & product to return as context in the view,
    allowing for dynamic button display, false is returned if the
    user hasn't added the product to their favorites.
    """

    product = get_object_or_404(Product, pk=product_id)
    review_form = PostReviewForm()
    reviews = Reviews.objects.filter(product=product)

    user = request.user
    if user.is_authenticated:
        favorite = Favorites.objects.filter(
            user=user,
            product=product
        )
    else:
        favorite = False

    context = {
        'product': product,
        'review_form': review_form,
        'reviews': reviews,
        'favorite': favorite,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """
    A view to allow superusers to add products to the store.

    Superuser credentials must first be verified.

    If the request method is POST, instantiate a new instance
    of the product form with the passed data and image files.
    Checks if form is valid, if so saves it and redirect to
    new product detail view. If there are any errors on the form,
    the original form request is passed back to them in the final
    else block.

    User feedback via Django messages and toasts is provided
    across every step.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to add product.\
                Please ensure the form is valid.'
            )
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    A view to allow superusers to edit products in the store.

    Superuser credentials must first be verified.

    Take in the request and the product ID the user is going to edit.
    Pre-fill the form by getting the product using get_object_or_404
    And then instantiating a product form using the product.

    If the request method is POST.
    Submit the form using request.post and request.files.
    Tell it the specific instance to update is the product obtained above.
    If the form is valid save it, add a success message
    and then redirect to the product detail page using the product ID.
    Otherwise, add an error message and return the form,
    which will have the errors attached.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to update product.\
                Please ensure the form is valid.'
            )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """
    A view to allow superusers to edit products in the store.

    Superuser credentials must first be verified.

    Takes in the request and the product id to be deleted.
    First collect the product with get_object_or_404,
    then call product.delete.
    Add a success message and redirect back to the all products page.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
