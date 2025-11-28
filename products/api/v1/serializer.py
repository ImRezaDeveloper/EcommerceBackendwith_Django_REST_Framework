from rest_framework import serializers
from products.models import ProductModel


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ["id", "name", "slug", "price", "description", "quantity", "discount_percent", "is_active"]