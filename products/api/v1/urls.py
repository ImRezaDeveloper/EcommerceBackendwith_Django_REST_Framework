from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductsList.as_view()),
    path('products/<str:pk>', views.ProductDetail.as_view())
]