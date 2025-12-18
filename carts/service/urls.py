from django.urls import path
from . import views

urlpatterns = [
    path('carts/', views.ItemsList.as_view(), name='carts'),
    path('carts/add', views.AddToCart.as_view(), name='add-to-carts')
]
