from rest_framework.validators import ValidationError
from products.models import CommentProduct, ProductModel
from rest_framework.response import Response

class CommentProductFilter():
    
     @staticmethod
     def get_comments_for_product(product_id: int):
        return CommentProduct.objects.filter(product_id=product_id)
     
class ProductFilter():
   
   @staticmethod
   def get_product_for_check_buy(user_id: int, product_id: int):
      if not ProductModel.objects.filter(user=user_id, id=product_id).exists():
         raise ValidationError({"detail": "you should first buy this product to leave comment"})
      
   @staticmethod
   def get_product_for_check_user_comment(user_id: int, product_id: int):
      if ProductModel.objects.filter(user=user_id, id=product_id).exists():
         raise ValidationError({"detail": "you've already leaved comment for this product"})
      
   # @staticmethod
   # def get_product_with_category()