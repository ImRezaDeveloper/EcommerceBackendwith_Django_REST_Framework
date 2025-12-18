from rest_framework.views import APIView
from .cart import CartService
from products.models import ProductModel
from products.api.v1.serializer import ProductSerializer
from rest_framework.response import Response

class ItemsList(APIView):
    
    def get(self, request):
        request.session.accessed = True
        # یا ساده‌تر:
        if not request.session.session_key:
            request.session.create()
            
        # user_id = request.user.id
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
    
    def post(self, request):
        # دریافت داده از درخواست
        product_id = request.data.get("product_id")
        quantity = request.data.get('quantity', 1)  # پیش‌فرض 1

        if not product_id:
            return Response({"error": "product_id is required"}, status=400)

        try:
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        # اضافه کردن به سبد خرید
        cart_service = CartService(request)  # معمولاً request یا user رو می‌گیره
        cart_service.add_item(product_id=product_id, quantity=quantity)

        # دریافت سبد خرید به‌روز شده
        cart_data = cart_service.get_items()  # فرضاً این متد وجود داره

        # سریالایز کردن محصولات موجود در سبد
        product_ids = [int(item) for item in cart_data.keys()]
        products = ProductModel.objects.filter(id__in=map(int, product_ids))
        serializer = ProductSerializer(products, many=True)

        # اضافه کردن quantity به هر آیتم
        data = []
        for item in serializer.data:
            pid = str(item['id'])
            item['quantity'] = cart_data.get(pid, {}).get('quantity', 0)
            data.append(item)

        return Response({"cart": data})