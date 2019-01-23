import logging

from rest_framework import serializers

from acmin.models import Field
from acmin.utils import import_class, attr

logger = logging.getLogger(__name__)


class BaseSerializer(serializers.ModelSerializer):
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


def get_serializer(model_class):
    app_name = model_class.__module__.split(".")[0]
    name = f"{model_class.__name__}Serializer"
    module = f'{app_name}.serializer'
    try:
        return import_class(f'{module}.{name}')
    except (ImportError, AttributeError, Exception):
        try:
            return type(f"Dynamic{name}", (BaseSerializer,), dict(
                Meta=type("Meta", (), dict(model=model_class)),
                __module__=module,
            ))
        except Exception as e:
            logger.error(e)
