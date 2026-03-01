"""
Docstring for core.views
"""

from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from core.models import PaginationSize
# Create your views here.


class StandardPageNumberPagination(PageNumberPagination):
    """
    For using pagination size from frontend like 20, 30, 50, etc.
    """

    page_size = 50 #default
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_page_size(self, request):
        
        requested_size = request.query_params.get(self.page_size_query_param)

        page_size_list = PaginationSize.objects.filter(is_active=True).values_list('data_per_page', flat=True)

        allowed_sizes = page_size_list

        if requested_size in allowed_sizes:
            return int(requested_size)
        
        return self.page_size
    


