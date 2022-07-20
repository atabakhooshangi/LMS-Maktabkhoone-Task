from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework import pagination


class MyCustomPaginator(pagination.PageNumberPagination):
    page_size =int(settings.REST_FRAMEWORK['PAGE_SIZE'])

    def get_paginated_response(self, data):
        return {
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        }