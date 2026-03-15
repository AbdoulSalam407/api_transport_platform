"""
Paginateurs personnalisés
"""
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """Pagination standard pour l'API"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class LargePagination(PageNumberPagination):
    """Large pagination pour les listes importantes"""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200
