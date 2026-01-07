from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from carts.service.serializer import CartItemsSerializer
from orders.service import checkout
from orders.service.checkout import CheckoutService
from django.core.cache import cache
from django.db import transaction
from orders.models import Order, OrderItems
from orders.api.v1.serializer import OrderAddressSerializer, OrderSerializer, OrderItemsSerializer

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            service = CheckoutService(request)
            order = service.checkout()
            
            transaction.on_commit(lambda: service.cart.clear_items())
            
            return Response(
                {"message": "Order created successfully", "order_id": order.id},
                status=status.HTTP_201_CREATED
            )
        
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print("Checkout error:", str(e))
            return Response(
                {"error": "An error occurred during checkout", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class OrdersList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = self.request.user.id
        orders = Order.objects.filter(id=user_id)
        serializer = OrderSerializer(orders, many=True)
        return Response({"orders": serializer.data})
    
class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        order_items = OrderItems.objects.filter(order__user=request.user, order__id=id)
        serializer = OrderItemsSerializer(order_items, many=True)
        return Response({"order_items": serializer.data})