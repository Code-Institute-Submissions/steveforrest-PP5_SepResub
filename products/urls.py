from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.all_products, name='products'),
    path('order/product/<str:pk>/', views.identify_product, name='product'),
]