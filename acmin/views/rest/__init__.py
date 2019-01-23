import logging

from rest_framework import viewsets, serializers
from rest_framework.response import Response

from acmin.models import Field
from acmin.utils import import_class, attr

logger = logging.getLogger(__name__)


class BaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = None

    def get_fields(self):
        fields = super().get_fields()
        return fields

    def get_field_names(self, declared_fields, info):
        request = attr(self, "_context.request")
        model = attr(self.Meta, "model")
        fields = Field.get_fields(request.user, model)
        names = [field.attribute for field in fields]

        return names


def find_serializer(model_class):
    app_name = model_class.__module__.split(".")[0]
    name = f"{model_class.__name__}Serializer"
    module = f'{app_name}.serializer'
    try:
        return import_class(f'{module}.{name}')
    except ImportError:
        try:
            return type(f"Dynamic{name}", (BaseSerializer,), dict(
                Meta=type("Meta", (), dict(model=model_class)),
                __module__=module,
            ))
        except Exception as e:
            logger.error(e)


class BaseViewSet(viewsets.ModelViewSet):
    class Meta:
        model = None

    def get_serializer_class(self):
        result = find_serializer(self.Meta.model)
        print(result)
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
            list=data,
            pagination=dict(
                total=count,
                pageSize=paginator.per_page,
                pages=paginator.num_pages,
                current=int(self.request.GET.get("page", 1))
            )))


def find_viewset(model_class):
    app_name = model_class.__module__.split(".")[0]
    name = f"{model_class.__name__}ViewSet"
    module = f'{app_name}.views'
    try:
        return import_class(f'{module}.{name}')
    except ImportError:
        try:
            return type(f"Dynamic{name}", (BaseViewSet,), dict(
                Meta=type("Meta", (), dict(
                    model=model_class
                )),
                __module__=module,
            ))
        except Exception as e:
            logger.error(e)
