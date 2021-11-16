from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/<int:category_id>/', views.products, name='products'),
    path('details/<int:product_id>', views.detail_product, name='detail_product'),
    path('registr/', views.registration, name='registr'),
    path("add-rating/", views.add_star_rating, name='add_rating'),
    path("add-comment/", views.add_comment, name='add_comment')
]
