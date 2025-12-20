from django.urls import path
from . import views

urlpatterns = [
    path('carts/', views.ItemsList.as_view(), name='carts'),
    path('carts/add', views.AddToCart.as_view(), name='add-to-carts'),
    path('carts/remove', views.RemoveFromCart.as_view(), name='remove-from-carts'),
    path('carts/clear', views.ClearCart.as_view(), name='clear-carts'),
    
]
