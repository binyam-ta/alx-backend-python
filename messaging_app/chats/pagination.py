from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    # Include total count in the paginated response
    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,   # <- required for the automated check
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data
        })
