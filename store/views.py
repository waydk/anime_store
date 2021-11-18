from django.shortcuts import render, redirect
from .forms import CommentForm, RatingForm, UserRegistrationForm
from django.http import HttpResponse
from django.utils import timezone
from django.template.defaulttags import register


from store.models import Categories, Comments, Product, Rating

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
    user_rating = Rating.objects.filter(product_id=product_id, author=request.user)

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
            new_rating.author = request.user
            # Check author
            user_rating = Rating.objects.filter(product_id=int(request.POST.get("product")), author=request.user)
            if user_rating:
                return HttpResponse(status=400)
            new_rating.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

# Custom filters
@register.filter
def get_items(value):
    return value.items()


@register.filter
def get_range(value):
    return range(value)
