from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class CustomLimitPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_num'
    page_size_query_param = 'page_size'
    max_page_size = 10
