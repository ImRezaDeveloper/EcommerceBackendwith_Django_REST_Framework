from rest_framework.views import APIView
from .cart import CartService
from products.models import ProductModel
from products.api.v1.serializer import ProductSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ItemsList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        request.session.accessed = True
        if not request.session.session_key:
            request.session.create()
            
        cart_service = CartService(request)
        cart_data = cart_service.get_items()
        
        products = ProductModel.objects.filter(id__in=map(int, cart_data.keys()))
        serializer = ProductSerializer(products, many=True)
        
        data = []
        for item in serializer.data:
            product_id = str(item['id'])
            item['quantity'] = cart_data[product_id]["quantity"]
            data.append(item)
            
        return Response({"cart:": data})
    
class AddToCart(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get('quantity', 1)
        product = ProductModel.objects.get(id=product_id)
        
        if product.stock == 0:
            return Response({"error": "quantity is not enough"}, status=400)

        if not product_id:
            return Response({"error": "product_id is required"}, status=400)

        try:
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        cart_service = CartService(request)  
        cart_service.add_item(product_id=product_id, quantity=quantity)

        cart_data = cart_service.get_items()
          
        product_ids = [int(item) for item in cart_data.keys()]
        products = ProductModel.objects.filter(id__in=map(int, product_ids))
        serializer = ProductSerializer(products, many=True)

    
        data = []
        for item in serializer.data:
            pid = str(item['id'])
            item['quantity'] = cart_data.get(pid, {}).get('quantity', 0)
            data.append(item)

        return Response({"cart": data})
    
class RemoveFromCart(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")
        
        
        if not product_id:
            return Response({"error": "product_id is required"}, status=400)
        
        try:
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
        
        cart_service = CartService(request)
        cart_service.remove_item(product_id=product_id, quantity=quantity)
        
        cart_data = cart_service.get_items()
        
        product_ids = [int(item) for item in cart_data.keys()]
        product = ProductModel.objects.filter(id__in=map(int, product_ids))
        serializer = ProductSerializer(product, many=True)
        
        return Response({"cart": serializer.data})
    
class ClearCart(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        cart_service = CartService(request)
        cart_service.clear_items()
        
        cart_data = cart_service.get_items()
        
        return Response({"cart": cart_data})