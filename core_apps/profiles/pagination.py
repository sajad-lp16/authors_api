from rest_framework.pagination import PageNumberPagination


class ProfilePagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page_number"
    max_page_size = 20
