from carts.service.cart import CartService
from orders.models import *
from products.models import ProductModel
from django.db import transaction


from django.db import transaction

class CheckoutService:
    def __init__(self, request):
        self.user = request.user
        self.cart = CartService(request)
        
    @transaction.atomic
    def checkout(self):
        cart_items = self.cart.get_items()
        
        if not cart_items:
            raise ValueError("Cart is empty")

        total_price = 0
        data = []
        
        
        for product_id, item in cart_items.items():
            product = ProductModel.objects.get(id=product_id)
            quantity = item["quantity"]
            
            total_price += product.price * quantity
          
            data.append({
                "product": product,
                "quantity": quantity,
                "price": product.price
            })
            
        product.stock = product.stock - quantity
        product.save()
        
        order = Order.objects.create(
            user=self.user,
            total_price=total_price
        )
        
        order_items = [
            OrderItems(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["price"]
            )
            for item in data
        ]
        OrderItems.objects.bulk_create(order_items)
        return order