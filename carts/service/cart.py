from django.core.cache import cache

class CartService:
    def __init__(self, request):
        self.request = request
        self.user = request.user

        if self.user:
            self.key = f"cart_user_{self.user}"
        else:
            if not request.session.session_key:
                request.session.create()
            self.key = f"cart_session_{request.session.session_key}"

    def get_items(self):
        return cache.get(self.key, {})

    def add_item(self, product_id, quantity=1):
        product_id = str(product_id)
        cart = cache.get(self.key, {})
        
        if product_id in cart:
            cart[product_id]["quantity"] += quantity
        else:
            cart[product_id] = {"quantity": quantity}

        cache.set(self.key, cart, timeout=86400)

    def remove_item(self, product_id, quantity):
        cart = cache.get(self.key) or {}
        product_id = str(product_id)

        if product_id in cart:
            cart[product_id]["quantity"] -= quantity

            if cart[product_id]["quantity"] <= 0:
                del cart[product_id]

        cache.set(self.key, cart, timeout=86400)

    def get_items(self):
        return cache.get(self.key) or {}

    def clear_items(self):
        return cache.delete(self.key) 