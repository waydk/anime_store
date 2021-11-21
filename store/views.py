from django.db import models
from django.shortcuts import render, redirect
from .forms import CommentForm, RatingForm, UserRegistrationForm
from django.http import HttpResponse
from django.utils import timezone
from django.template.defaulttags import register


from store.models import Categories, Comments, Favorite, Product, Rating, ShopCart

# Helpers
def mean(numbers: list):
    """Average value
    """
    return float(sum(numbers)) / max(len(numbers), 1)

# Views
def index(request):
    """Home page
    """
    categories = Categories.objects.all()
    return render(request, 'store/index.html', {'categories': categories})

def products(request, category_id):
    """Product page
    """
    products = Product.objects.filter(category_id=category_id)
    title = Categories.objects.get(id=category_id)
    return render(request, 'store/products.html', {'products': products, 'title': title})


def detail_product(request, product_id):
    """Detail product page
    """
    product = Product.objects.get(id=product_id)
    product_comments = Comments.objects.filter(product_id=product_id, on_moderation=False)
    ratings = Rating.objects.filter(product_id=product_id)
    ratings = [int(str(rating.star)) for rating in ratings]
    average_rating = int(mean(ratings))

    # Check comment
    show_comment = None
    user_comment = Comments.objects.filter(product_id=product_id, author=request.user)

    # Is there a user comment on this product
    if user_comment:
        # In moderation
        if user_comment[0].on_moderation:
            show_comment = 'Ваш комментарий на модерации'
        # Not moderation
        if not user_comment[0].on_moderation:
            show_comment = 'Вы уже писали комментарий под данным продуктом'

    # Check rating
    show_rating = None
    user_rating = Rating.objects.filter(product_id=product_id, user=request.user)

    if user_rating:
        show_rating = 'Вы уже оценивали данный товар'

    return render(request, 'store/product_detail.html',
                  {'product': product, 'comments': product_comments,
                   'comment_form': CommentForm, 'star_form': RatingForm(),
                   'average_rating': average_rating, 'show_comment': show_comment,
                   'show_rating': show_rating})


def registration(request):
    """Registration product page
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'registration//register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/registr.html', {'user_form': user_form})

# Comments and rating

def add_comment(request):
    """Product comment
    """
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product_id = int(request.POST.get("product"))
            comment.author = request.user
            comment.on_moderation = True
            comment.pub_date = timezone.now()
            comment.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponse(status=400)


def add_star_rating(request):
    """Rating product
    """
    if request.method == "POST":
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            new_rating = rating_form.save(commit=False)
            new_rating.product_id = int(request.POST.get("product"))
            new_rating.star_id = int(request.POST.get("star"))
            new_rating.user = request.user
            # Check user
            user_rating = Rating.objects.filter(product_id=int(request.POST.get("product")), user=request.user)
            if user_rating:
                return HttpResponse(status=400)
            new_rating.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

# Cart and Favorite

def show_cart_or_favorite(request, favorite=False, cart=False):
    """Show cart or favorite
    """
    if cart:
        model = Favorite
    if favorite:
        model = ShopCart
    items = model.objects.filter(user=request.user)
    total_price = sum([item.product.price for item in items])
    if cart:
        return render(request, 'store/shop_cart.html', {'items_cart': items, 'total_price': float(total_price)})
    if favorite:
        return render(request, 'store/favorite.html', {'items_favorite': items, 'total_price': float(total_price)})

def shop_cart(request):
    """Show shop cart
    """
    return show_cart_or_favorite(request, cart=True)


def favorite(request):
    """Show favorite
    """
    return show_cart_or_favorite(request, favorite=True)


def add_to_cart_or_favorite(request, product_id, cart=False, favorite=False):
    """Add cart or favorite
    """
    product = Product.objects.get(id=product_id)
    if cart:
        model = ShopCart
    if favorite:
        model = Favorite

    # Repeat check
    item = model.objects.filter(user=request.user, product=product_id)
    items = model.objects.filter(user=request.user)
    total_price = sum([item.product.price for item in items])
    if item:
        if cart:
            return render(request, 'store/shop_cart.html',
                          {'items_cart': items, 'total_price': float(total_price)})
        if favorite:
            return render(request, 'store/favorite.html',
                          {'items_favorite': items, 'total_price': float(total_price)})
    if cart:
        new_item = ShopCart()
    if favorite:
        new_item = Favorite()

    new_item.user = request.user
    new_item.product = product
    new_item.price = product.price
    new_item.save()

    if cart:
        return render(request, 'store/shop_cart.html', {'items_cart': items, 'total_price': float(total_price)})
    if favorite:
        return render(request, 'store/favorite.html', {'items_favorite': items, 'total_price': float(total_price)})


def add_to_shop_cart(request, product_id):
    """Add and show shop cart
    """
    return add_to_cart_or_favorite(request, product_id, cart=True)


def add_to_favorite(request, product_id):
    """Add and show favorite
    """
    return add_to_cart_or_favorite(request, product_id, favorite=True)


# Custom filters
@register.filter
def get_items(value):
    return value.items()


@register.filter
def get_range(value):
    return range(value)
