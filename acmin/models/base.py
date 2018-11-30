from django.db import models
from django.db.models.base import ModelBase
from django.urls import reverse

from acmin.utils import attr


class BasePermission:
    creatable = True
    editable = True
    removable = True
    cloneable = True
    exportable = True
    viewable = True

    def __init__(self, **kwargs):
        self.creatable = kwargs.get("creatable", True)
        self.editable = kwargs.get("editable", True)
        self.removable = kwargs.get("removable", True)
        self.cloneable = kwargs.get("cloneable", True)
        self.exportable = kwargs.get("exportable", True)
        self.viewable = kwargs.get("viewable", True)

    @property
    def operable(self):
        return self.viewable or self.removable or self.cloneable


def merge(name, attrs, meta_name, base_meta):
    meta = attrs.pop(meta_name, None)
    if not meta:
        meta = type(meta_name, (base_meta,), dict(
            __module__=f'{attrs.get("__module__")}.{name}'
        ))
    attributes = vars(meta)
    for key, value in vars(base_meta).items():
        if ("__init__" == key or not key.startswith("_")) and "abstract" != key and key not in attributes:
            setattr(meta, key, value)
    return meta


class BaseMeta(ModelBase):
    def __new__(mcs, name, bases, attrs, **kwargs):
        if name != 'AcminModel':
            attrs["Meta"] = merge(name, attrs, "Meta", getattr(AcminModel, "Meta"))
            attrs["_permission"] = merge(name, attrs, "Permission", BasePermission)
        return ModelBase.__new__(mcs, name, bases, attrs, **kwargs)


class AcminModel(models.Model, metaclass=BaseMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        clazz = attr(self.__class__, "_permission")
        self._permission = clazz(**{key: value for key, value in vars(clazz).items() if not key.startswith("_")})

    class Meta:
        ordering = ['-id']
        abstract = True

    @property
    def permission(self) -> BasePermission:
        return self._permission

    def get_absolute_url(self):
        return reverse(self.__class__.__name__ + "-update", kwargs={"pk": self.pk})

    @property
    def color(self):
        return "black"
