from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    """
        Pagination products by page_size
    """
    page_size = 1
    page_query_param = "page"
    max_page_size = 100