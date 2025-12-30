from rest_framework import serializers
from orders.models import Order, OrderItems, OrderAddress

class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ("id", "status", "total_price", "user")
        
class OrderItemsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItems
        fields = '__all__'

class OrderAddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderAddress
        fields = '__all__'