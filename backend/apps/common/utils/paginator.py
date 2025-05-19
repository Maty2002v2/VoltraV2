from django.urls import reverse
from rest_framework import pagination
from rest_framework.response import Response


class CurrentPagePagination(pagination.PageNumberPagination):
    def get_all_page_links(self):
        links = []
        url_name = self.request.resolver_match.url_name
        server_url = self.request.build_absolute_uri('/')[:-1]
        if url_name:
            base_url = reverse(self.request.resolver_match.url_name)
            query_params = self.request.GET.copy()

            for page_num in range(1, self.page.paginator.num_pages + 1):
                query_params['page'] = page_num
                links.append(f'{server_url}{base_url}?{query_params.urlencode()}')

        return links

    def get_paginated_response(self, data):
        return Response({
            'links': self.get_all_page_links(),
            'page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'results': data,
            'page_size': self.page_size,
        })
