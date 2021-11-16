from django.contrib import admin
from .models import Comments, Product, Categories, Rating, RatingStar

# Register your models here.
admin.site.register(Product)
admin.site.register(Categories)
admin.site.register(Comments)
admin.site.register(Rating)
admin.site.register(RatingStar)
