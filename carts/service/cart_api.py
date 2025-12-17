from rest_framework.views import APIView
from cart import CartService

class ItemsList(APIView):
    
    def get(self):
        user_id = self.request.user
        cart_service = CartService(user_id)
        cart_data = cart_service.get_items()