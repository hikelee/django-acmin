from django.db import models

from acmin.cache import clear
from acmin.models import ModelMixin
from acmin.utils import attr, get_model_fields_without_relation


class BaseModel(models.Model, ModelMixin):
    class Meta:
        abstract = True

    created = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    modified = models.DateTimeField('更新时间', auto_now=True)

    def save(self, *args, **kwargs):
        clear(self.__class__)
        super().save(*args, **kwargs)

    def to_json(self, include_fields=[], exclude_fields=[]):
        fields = include_fields
        if not fields:
            fields = [f for f in get_model_fields_without_relation(self.__class__) if f not in exclude_fields]
        return {key: attr(self, key) for key in fields}
