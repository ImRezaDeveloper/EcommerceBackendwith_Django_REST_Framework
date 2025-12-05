from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializer import UserRegisterSerializer


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