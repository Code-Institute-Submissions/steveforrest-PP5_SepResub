from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_order, name='view_order'),
    path('add/<item_id>/', views.add_to_order, name='add_to_order'),
]
