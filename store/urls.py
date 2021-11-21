from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/<int:category_id>/', views.products, name='products'),
    path('details/<int:product_id>', views.detail_product, name='detail_product'),
    path('registr/', views.registration, name='registr'),
    path("add-rating/", views.add_star_rating, name='add_rating'),
    path("add-comment/", views.add_comment, name='add_comment'),
    path('cart/', views.shop_cart, name='shop_cart'),
    path('add_to_cart/<int:product_id>', views.add_to_shop_cart, name='add_to_cart'),
    path('favorite/', views.favorite, name='favorite'),
    path('add_to_favorite/<int:product_id>', views.add_to_favorite, name='add_to_favorite')
]
