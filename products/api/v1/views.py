from django.http import Http404
from rest_framework.exceptions import JsonResponse, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from accounts.models import User
from products.api.v1.serializer import ProductSerializer, CommentProductSerializer, CategoriesSerializer
from products.models import ProductModel, CommentProduct, CategoryModel
from rest_framework.response import Response
from rest_framework import generics, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import ProductPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .throttling import CustomAnonRateThrottle


class ProductsList(generics.ListAPIView):
    """
        :return
            return all products
    """
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['in_stock']
    search_fields = ["name"]
    # ordering
    ordering_fields = ["price"]
    # pagination
    pagination_class = ProductPagination
    # throttling
    throttle_classes = [UserRateThrottle, CustomAnonRateThrottle]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = ProductModel.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"data": serializer.data})


class ProductDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.ListAPIView):

    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

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
    # permission_classes = [IsAuthenticated]
    """
    Returns all comments related to a specific product.

    Parameters:
        pk (int): The ID of the product whose comments you want to retrieve.

    Responses:
        200 OK: Successfully returned the list of comments.
        400 Bad Request: Invalid product ID or request parameters.
    """
    def get_queryset(self):
        product_id = self.kwargs.get('id')
        return CommentProduct.objects.filter(product_id=product_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "There is no comment for this product"}, status=404)
        return super().list(request, *args, **kwargs)

    serializer_class = CommentProductSerializer


class CommentCreateProducts(generics.ListCreateAPIView):
        """
            Create comment that related to a specific product.

            Parameters:
                pk (int): The ID of the product that comment should be save for that.

            Responses:
                201 OK: Successfully created the comment.
                400 Bad Request: Invalid product ID or request parameters.
        """

        serializer_class = CommentProductSerializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            product_id = self.kwargs.get('id')
            return CommentProduct.objects.filter(product_id=product_id)

        def perform_create(self, serializer):
            """
            this method create comment for each product
            :param
                pk: id of the each product
            Responses:
                201 OK: Successfully created the comment.
                400 Bad Request: Invalid product ID or request parameters.
            """
            product_id = self.kwargs.get('id')
            user = self.request.user

            if CommentProduct.objects.filter(user=user, product_id=product_id).exists():
                raise ValidationError({"detail": "you've already leaved comment for this product"})

            serializer.save(user=user, product_id=product_id)


class CategoriesList(generics.ListAPIView):
    """
        Returns all CategoryList.

        Responses:
            200 OK: Successfully returned the list of category.
            400 Bad Request: Invalid category ID or request parameters.
        """
    def get_queryset(self):
        category_name = self.kwargs.get('category')
        return ProductModel.objects.filter(categories__name=category_name)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "There is no category for this product"}, status=404)
        return super().list(request, *args, **kwargs)

    serializer_class = CategoriesSerializer
