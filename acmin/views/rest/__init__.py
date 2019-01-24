import logging

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from acmin.models import Permission, PermissionItem
from acmin.serializer import get_serializer
from acmin.utils import import_class, attr

logger = logging.getLogger(__name__)


class BaseViewSet(viewsets.ModelViewSet):
    class Meta:
        model = None

    def get_serializer_class(self):
        result = get_serializer(self.Meta.model)
        return result

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        return serializer

    def get_queryset(self):
        model = attr(self, "Meta.model")
        return model.objects.all()

    def get_paginated_response(self, data):
        paginator = self.paginator.page.paginator
        count = paginator.count
        return Response(dict(
            data=(dict(list=data, total=count)),
            status=200,
            message="success"
            # list=data,
            # pagination=dict(
            #    total=count,
            #    pageSize=paginator.per_page,
            #    pages=paginator.num_pages,
            #    current=int(self.request.GET.get("page", 1))

        ))


class ViewPermission(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and Permission.has_permission(request.user, view.Meta.model, PermissionItem.listable)


class AuthenticatedBaseViewSet(BaseViewSet):
    permission_classes = (ViewPermission,)


def get_viewset(model_class, login_required=True):
    app_name = model_class.__module__.split(".")[0]
    name = f"{model_class.__name__}ViewSet"
    module = f'{app_name}.views'
    try:
        return import_class(f'{module}.{name}')
    except(ImportError, AttributeError, Exception):
        super_class = AuthenticatedBaseViewSet if login_required else BaseViewSet
        return type(f"Dynamic{name}", (super_class,), dict(
            Meta=type("Meta", (), dict(
                model=model_class
            )),
            __module__=module,
        ))
