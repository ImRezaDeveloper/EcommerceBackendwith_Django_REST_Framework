from carts.service.cart import CartService
from orders.models import *
from products.models import ProductModel
from django.db import transaction


from django.db import transaction

class CheckoutService:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.cart = CartService(request)

    @transaction.atomic
    def checkout(self):
        cart_items = self.cart.get_items()
        if not cart_items:
            raise ValueError("Cart is empty")

        total_price = 0
        data = []

        province = self.request.data.get("province")
        city = self.request.data.get("city")
        address = self.request.data.get("address")
        phone_number = self.request.data.get("phone_number")
        postal_code = self.request.data.get("postal_code")

        for product_id, item in cart_items.items():
            product = ProductModel.objects.get(id=product_id)
            quantity = item["quantity"]

            total_price += product.price * quantity

            data.append({
                "product": product,
                "quantity": quantity,
                "price": product.price,
            })

        order = Order.objects.create(
            user=self.user,
            total_price=total_price,
        )

        user_address = OrderAddress.objects.create(
            order=order,
            user=self.user,
            province=province,
            city=city,
            address=address,
            phone_number=phone_number,
            postal_code=postal_code
        )

        order.address = user_address
        order.save()

        for item in data:
            OrderItems.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["price"],
            )

        self.cart.clear_items()

        return order
