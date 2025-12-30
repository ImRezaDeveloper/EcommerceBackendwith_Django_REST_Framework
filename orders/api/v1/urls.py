
from django.urls import path
from .views import CheckoutView, OrdersList, OrderDetail

urlpatterns = [
    path("checkout/", CheckoutView.as_view()),
    path("orders/me", OrdersList.as_view()),
    path("orders/me/detail/<int:id>/", OrderDetail.as_view())
]