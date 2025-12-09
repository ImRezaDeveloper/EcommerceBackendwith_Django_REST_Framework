from rest_framework import serializers
from accounts.models import User


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("phone",)

    def validate(self, attrs):
        phone = attrs.get("phone")

        if not phone.startswith("09"):
            raise serializers.ValidationError({"phone": "phone number should be start with 09"})

        if len(phone) != 11:
            raise serializers.ValidationError({"phone": "phone number must be exactly 11 characters"})

        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({"phone": "this phone number already registered in our website"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(phone=validated_data["phone"])
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "email", "phone", "is_active")

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)