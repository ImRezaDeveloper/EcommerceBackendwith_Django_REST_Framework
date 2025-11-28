from django.http import Http404

from products.api.v1.serializer import ProductSerializer, CommentProductSerializer, CategoriesSerializer
from products.models import ProductModel, CommentProduct, CategoryModel
from rest_framework.response import Response
from rest_framework import generics, mixins
from django_filters.rest_framework import DjangoFilterBackend


class ProductsList(generics.ListAPIView):
    """
        :return
            return all products
    """
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['in_stock']

class ProductDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.ListAPIView):

    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        """
            Get Product with pk
            :return:
                :response:
                    200 -> ok
                    404 -> product not found with invalid id

            :parameter
                pk


        """
        return super().retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
            Update Product with pk
            :parameter:
                request: new_data that client send
                pk: id of each product
            :return:
                :response:
                    - 200 OK
                    - 400 Bad Request -> if data is invalid
                    - 404 Not Found   -> اif product does not exist
        """
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
            Delete Product with pk
            :return:
                :response:
                    - 204
                    - 404
        """
        return super().destroy(request, *args, **kwargs)


class CommentProductList(generics.ListAPIView):

    def get_queryset(self):
        product_id = self.kwargs.get('id')
        return CommentProduct.objects.filter(product_id=product_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "There is no comment for this product"}, status=404)
        return super().list(request, *args, **kwargs)

    serializer_class = CommentProductSerializer


class CategoriesList(generics.ListAPIView):

    def get_queryset(self):
        category_name = self.kwargs.get('category')
        return ProductModel.objects.filter(categories__name=category_name)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "There is no category for this product"}, status=404)
        return super().list(request, *args, **kwargs)

    serializer_class = CategoriesSerializer
