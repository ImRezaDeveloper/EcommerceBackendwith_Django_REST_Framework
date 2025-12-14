from rest_framework import serializers
from products.models import ProductModel, CommentProduct


class CommentProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentProduct
        exclude = ('created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    rating_count = serializers.IntegerField(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = ProductModel
        fields = ["id", "name", "price", "description", "quantity", "rating_count", "avg_rating", "discount_percent", "is_active"]


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ["id", "name", "slug", "price", "description", "quantity", "discount_percent", "is_active"]
