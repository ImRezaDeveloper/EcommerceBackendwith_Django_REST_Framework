from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from carts.service.serializer import CartItemsSerializer
from orders.service import checkout
from orders.service.checkout import CheckoutService
from django.core.cache import cache
from django.db import transaction

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            service = CheckoutService(request)
            order = service.checkout()  # حالا order واقعاً شیء Order هست
            
            # پاک کردن سبد خرید فقط بعد از commit موفق
            transaction.on_commit(lambda: service.cart.clear_items())
            
            return Response(
                {"message": "Order created successfully", "order_id": order.id},
                status=status.HTTP_201_CREATED
            )
        
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # برای دیباگ موقت
            print("Checkout error:", str(e))
            return Response(
                {"error": "An error occurred during checkout", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
