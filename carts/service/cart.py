from django.core.cache import cache

class CartService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.key = f'cart:{user_id}'
    
    # add item to cart
    def add_item(self, product_id, quantity):
        cart = cache.get(self.key) or {}
        if str(product_id) in cart:
            cart[str(product_id)] += quantity
        else:
            cart[str(product_id)] = quantity
        
        cache.set(self.user_id, cart, timeout=86400)
        
    # remove item from cart
    def remove_item(self, product_id, quantity):
        cart = cache.get(self.key) or {}
        if str(product_id) in cart:
            cart[str(product_id)] -= quantity
            if (str(product_id)) <= 0:
                del cart[str(product_id)]
        
        cache.set(self.user_id, cart, timeout=86400)
        
    # get all items from cart
    def get_items(self):
        return cache.get(self.key) or {}
    
    # delete all items in cart
    def clear_cart(self):
        cache.delete(self.key)