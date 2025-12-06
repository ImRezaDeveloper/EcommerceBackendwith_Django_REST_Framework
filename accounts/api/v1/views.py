from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from .serializer import UserRegisterSerializer, UserSerializer
from rest_framework import generics


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

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserInfoById(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)