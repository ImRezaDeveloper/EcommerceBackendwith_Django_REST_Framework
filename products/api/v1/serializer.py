from rest_framework import serializers
from products.models import ProductModel, CommentProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ["id", "name", "price", "description", "quantity", "discount_percent", "is_active"]


class CommentProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentProduct
        exclude = ('created_at', 'updated_at')


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ["id", "name", "slug", "price", "description", "quantity", "discount_percent", "is_active"]
