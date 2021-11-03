from django.shortcuts import render

from store.models import Categories, Product

# Create your views here.
def index(request):
    categories = Categories.objects.all()
    context = {'categories': categories}
    return render(request, 'store/index.html', context)

def products(request, category_id):
    products = Product.objects.filter(category_id=category_id)
    title = Categories.objects.get(id=category_id)
    return render(request, 'store/products.html', {'products': products, 'title': title})
