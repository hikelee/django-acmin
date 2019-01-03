from rest_framework import viewsets
from rest_framework.response import Response


class BaseViewSet(viewsets.ModelViewSet):

    def perform_create(self, serializer):
        # serializer.save(owner=self.request.user)
        serializer.save()

    def get_paginated_response(self, data):
        paginator = self.paginator.page.paginator
        count = paginator.count
        return Response(dict(
            list=data,
            pagination=dict(
                total=count,
                pageSize=paginator.per_page,
                pages=paginator.num_pages,
                current=int(self.request.GET.get("page", 1))
            )))
