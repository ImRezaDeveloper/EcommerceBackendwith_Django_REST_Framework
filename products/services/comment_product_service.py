from products.models import CommentProduct
from rest_framework.response import Response

class CommentProductFilter():
    
     @staticmethod
     def get_comments_for_product(product_id: int):
        return CommentProduct.objects.filter(product_id=product_id)