from products.api.v1.serializer import ProductSerializer
from products.models import ProductModel
from rest_framework.response import Response
from rest_framework import generics, mixins


class ProductsList(generics.ListAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.ListAPIView):

    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)