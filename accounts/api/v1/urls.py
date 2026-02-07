from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from . import views

urlpatterns = [
    # login via jwt
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # logout
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # register => after register get jwt code
    path('register/', views.UserRegisterView.as_view(), name='register'),
    # path("verify-otp/", views.VerifyOtp.as_view(), name="verify-otp"),

    # user info
    path('users/', views.ListUserInfo.as_view(), name='users_info'),
    path('users/<str:pk>/', views.UserInfoById.as_view(), name='user_by_id'),
    path('users/me', views.UserProfile.as_view(), name="user_profile"),
    
    # password
    path("change_password/<int:id>", views.ChangePassword.as_view(), name="change_password")
]