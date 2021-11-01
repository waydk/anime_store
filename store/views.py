from django.http.response import HttpResponse
from django.template import loader

from store.models import Product

# Create your views here.
def index(request):
    latest_product_list = Product.objects.order_by('-pub_date')[:5]
    template = loader.get_template('store/index.html')
    context = {
        'latest_product_list': latest_product_list,
    }
    return HttpResponse(template.render(context, request))
