from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from .serializer import UserRegisterSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework import generics, status
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from ...permissions import IsOwner
from accounts.tasks import send_test_email
import random
from django.core.cache import cache
class UserRegisterView(APIView):
    """
        Register user with phone number
        Responses:
                201 OK: Successfully created the user.
                400 
                
                
                
                Bad Request: Invalid User or request parameters.
    """
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            print("this is otp code: ", otp_code)
            # print("Data from serializer:", serializer.data)
            # send_test_email.delay(serializer.data['email'], serializer.data['full_name'])
            return Response(
                {
                    "message": "User Registred Successfully"
                }, status=201
            )
            
        return Response(serializer.errors, status=400)


class ListUserInfo(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    

class UserInfoById(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        otp_code = cache.set("otp_", random.randint(100000, 999999))
        print(cache.get("otp_code"))
        return super().retrieve(request, *args, **kwargs)

    def put(self, request,*args, **kwargs):
        # if not self.check_user():
        #     return Response({"detail": "You cannot change other users"}, status=403)
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # check user for permission
    # def check_user(self):
    #     pk = self.kwargs.get('pk')
    #     user = get_object_or_404(User, id=pk)
    #     return user == self.request.user


class ChangePassword(generics.GenericAPIView):
    
    serializer_class = ChangePasswordSerializer
    
    def get_object(self):
        user_id = self.kwargs.get('id')
        return User.objects.get(pk=user_id)
    
    def put(self, request):

        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = request.data["old_password"]
        new_password = request.data["new_password"]

        user = self.get_object()
        if not user.check_password(raw_password=old_password):
            return Response(data={"error": "password does not match"}, status=400)
        else:
            user.set_password(new_password)
            user.save()
            return Response(data={"success": "password changed successfully!"}, status=200)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"detail": "Refresh token missing"}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()   # مهم!
        except Exception:
            return Response({"detail": "Invalid refresh token"}, status=400)

        return Response({"detail": "Logged out"}, status=205)


class UserProfile(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
# class VerifyOtp(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request):
#         # otp_code = 