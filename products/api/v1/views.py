import hashlib
from django.db.models import Avg, Count
from django.http import Http404
from rest_framework.exceptions import JsonResponse, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from accounts.models import User
from products.api.v1.serializer import ProductSerializer, CommentProductSerializer, CategoriesSerializer, WishListCreateProductSerializer, WishListProductsSerializer
from products.models import ProductModel, CommentProduct, CategoryModel, WishListProduct
from rest_framework.response import Response
from rest_framework import generics, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import ProductPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .throttling import CustomAnonRateThrottle
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from config.utils import delete_cache
from django.core.cache import caches
from django.core.cache import cache
from django.utils.http import quote_etag
from products.selector.get_products import get_all_products, get_product_by_id, get_all_comments
from products.services.product import CommentProductFilter, ProductFilter
from .permissions import IsOwnerForEdit
from zoneinfo import ZoneInfo
import jdatetime
from datetime import datetime, timedelta

class ProductsList(generics.ListAPIView):
    """
        :return
            return all products
    """
    queryset = get_all_products()
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
    # pagination_class = [IsAuthenticated]
    # cache key prefix
    CACHE_KEY_PREFIX = 'product_view'
    CACHE_TIME_OUT = 300
    
    def get_queryset(self):
        return ProductModel.objects.annotate(
            avg_rating=Avg("comments__rating"),
            rating_count=Count("comments__rating")
        )
    
    def get(self, request, *args, **kwargs):

        cache_key = f"{self.CACHE_KEY_PREFIX}|{request.path}"
        cached = cache.get(cache_key)
    
        last_updated = self.queryset.order_by('-updated_at').first().updated_at.isoformat()
        etag = quote_etag(hashlib.md5(last_updated.encode()).hexdigest())

        if request.headers.get("If-None-Match") == etag:
            return Response(status=304)
        
        if cached:
            print("CACHE HIT")
            return Response({"data": cached}, headers={"ETag": etag})

        response = get_all_products()
        serializer = ProductSerializer(response, many=True)
        data = serializer.data

        cache.set(cache_key, data, self.CACHE_TIME_OUT)
        print("CACHE SET")

        return Response(data, headers={"ETag": etag})


class ProductDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.ListAPIView):
    queryset = get_all_products()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    CACHE_KEY_PREFIX = 'product_view'
    CACHE_TIME_OUT = 300
    
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
        pk = kwargs["pk"]
        cache_key = f"{self.CACHE_KEY_PREFIX}:{pk}"
        
        cached = cache.get(cache_key)
        if cached:
            print("CACHE HIT")
            return Response(cached)
        
        product = self.get_object()
        serializer = ProductSerializer(product)
        data = serializer.data
        cache.set(cache_key, data, self.CACHE_TIME_OUT)
        
        print("CACHE SET")
        return Response({"data": serializer.data})

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
        delete_cache(self.CACHE_KEY_PREFIX)
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

    def get_queryset(self):
        return ProductModel.objects.annotate(
            avg_rating=Avg("comments__rating"),
            rating_count=Count("comments__rating")
        )


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
        product_id = self.kwargs.get("id")
        return CommentProductFilter.get_comments_for_product(product_id=product_id)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "There is no comment for this product"}, status=404)
        return super().list(request, *args, **kwargs)

    serializer_class = CommentProductSerializer
    
class CommentProductDetail(generics.RetrieveUpdateAPIView):
    queryset = CommentProduct.objects.all()
    serializer_class = CommentProductSerializer

    def update(self, request, *args, **kwargs):
        comment_pk = self.kwargs.get("comment_pk")
        try:
            comment = CommentProduct.objects.get(pk=comment_pk)
        except CommentProduct.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=404)

        now = datetime.now(ZoneInfo("Asia/Tehran"))

        created_at_local = comment.created_at.astimezone(ZoneInfo("Asia/Tehran"))

        if now - created_at_local > timedelta(minutes=1):
            return Response(
                {"detail": "You can't edit your comment after 1 minute."},
                status=400
            )

        return super().update(request, *args, **kwargs)
        

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
            return CommentProductFilter.get_comments_for_product(product_id=product_id)
        
        def print_services(self):
            product_id = self.kwargs.get('id')
            user = self.request.user
            
            ProductFilter.get_product_for_check_buy(user_id=user, product_id=product_id)
            ProductFilter.get_product_for_check_user_comment(user_id=user, product_id=product_id)

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
            
            self.print_services()

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


class WishListProductsView(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        wishlists = WishListProduct.objects.filter(user=self.request.user, is_deleted=False)
        return wishlists
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"detail": "your favorite list is empty."})
        # if queryset.exists():
        #     return Response({"detail": "this product is already added to your favorite product"}, status=200)
        return super().list(request, *args, **kwargs)
    
    
    serializer_class = WishListProductsSerializer
    
class WishListProductsCreateView(generics.CreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = WishListCreateProductSerializer
    
    def perform_create(self, serializer):
        product_id = serializer.validated_data['product']
        
        if WishListProduct.objects.filter(
            user=self.request.user,
            product_id=product_id,
            is_deleted=False
        ).exists():
            raise ValidationError("This product is already in your wishlist.")
        
        serializer.save(user=self.request.user)