from rest_framework import pagination
from rest_framework.response import Response


class PageNumberPagination(pagination.PageNumberPagination):
    page_size = 2
    max_page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'total_items': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'prev_page': bool(self.get_previous_link()),
            'next_page': bool(self.get_next_link()),
            'data': data
        })
