from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from . import views

urlpatterns = [
    # login via jwt
    path('api/v1/accounts/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # register => after register get jwt code
    path('api/v1/accounts/register', views.UserRegisterView.as_view(), name='register'),

    # user info
    path('api/v1/users/', views.ListUserInfo.as_view(), name='users_info'),
    path('api/v1/users/<str:pk>/', views.UserInfoById.as_view(), name='user_by_id'),
    
    # password
    path("change_password/<int:id>", views.ChangePassword.as_view(), name="change_password")
]