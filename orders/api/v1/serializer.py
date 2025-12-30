from rest_framework import serializers
from orders.models import Order, OrderItems, OrderAddress
        
class OrderItemsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItems
        fields = '__all__'

class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = ["province", "city", "address", "phone_number", "postal_code"]

class OrderSerializer(serializers.ModelSerializer):
    address = OrderAddressSerializer(many=True)  # nested serializer

    class Meta:
        model = Order
        fields = ("id", "status", "total_price", "user", "address")
