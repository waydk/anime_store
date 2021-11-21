from django.contrib import admin

from store.views import add_to_shop_cart
from .models import Comments, Favorite, Product, Categories, Rating, RatingStar, ShopCart

# Register your models here.
admin.site.register(Product)
admin.site.register(Categories)
admin.site.register(Comments)
admin.site.register(Rating)
admin.site.register(RatingStar)
admin.site.register(ShopCart)
admin.site.register(Favorite)
