from products.models import ProductModel, CommentProduct
from rest_framework.response import Response

def get_all_products():
    return ProductModel.objects.all()

def get_product_by_id(pk: str) -> ProductModel:
    return ProductModel.objects.get(pk=pk)

def get_all_comments(pk: str) -> ProductModel:
    return CommentProduct.objects.get(pk=pk)