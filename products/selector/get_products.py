from products.models import ProductModel
from rest_framework.response import Response

def get_all_products():
    return ProductModel.objects.all()

def get_product_by_id(pk: str) -> ProductModel:
    return ProductModel.objects.get(pk=pk)