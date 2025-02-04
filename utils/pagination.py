from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "per_page"
    max_page_size = 100

    def get_paginated_response(self, data):
        return {
            "page": self.page.number,
            "per_page": self.page.paginator.per_page,
            "count": self.page.paginator.count,
            "results": data,
        }
