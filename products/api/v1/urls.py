from django.urls import path
from . import views

urlpatterns = [
    # Products urls
    path('products/', views.ProductsList.as_view()),
    path('products/<str:pk>', views.ProductDetail.as_view()),

    # CommentsProducts urls
    path('products/<int:id>/reviews', views.CommentProductList.as_view()),
    path('products/<int:id>/create-review', views.CommentCreateProducts.as_view()),
    path('products/<str:pk>/reviews/edit', views.CommentProductDetail.as_view()),
    

    # categories
    path('categories/<str:category>/products/', views.CategoriesList.as_view())
]