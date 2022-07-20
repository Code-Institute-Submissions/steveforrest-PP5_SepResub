from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.all_products, name='products'),
    path('order/product/<int:id>/', views.identify_product, name='product'),
    path('order/product_search/', views.all_products, name='search_result'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:id>/', views.edit_product, name='edit_product'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),
    path('detail/<int:id>/', views.product_detail, name='detail_product'),
    path('review/<int:id>/', views.CreateReview.as_view(), name='create_review'),

]
