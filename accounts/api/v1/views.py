from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from .serializer import UserRegisterSerializer, UserSerializer
from rest_framework import generics
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class UserRegisterView(APIView):
    """
        Register user with phone number
        Responses:
                201 OK: Successfully created the user.
                400 Bad Request: Invalid User or request parameters.
    """
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
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
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)