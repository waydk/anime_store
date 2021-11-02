
from django.shortcuts import render

from store.models import Categories

# Create your views here.
def index(request):
    categories = Categories.objects.all()
    context = {'categories': categories}
    return render(request, 'store/index.html', context)
