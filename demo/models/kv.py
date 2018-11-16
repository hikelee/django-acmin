from acmin.utils import attr
from django.db import models
from python_utils import converters

from .base import BaseModel


class KeyValue(BaseModel):
    search_fields = ['key', 'value']

    class Meta:
        ordering = ['-id']
        verbose_name = verbose_name_plural = '键值对'

    key = models.CharField('Key', max_length=50, unique=True)
    value = models.TextField("Value")

    def __str__(self):
        return self.key

    @classmethod
    def get_string(cls, key, default=None):
        value = attr(cls.objects.filter(key=key).first(), "value")
        if value is None:
            value = default
        return value

    @classmethod
    def get_int(cls, key, default=0):
        return converters.to_int(cls.get_string(key), default)

    @classmethod
    def get_bool(cls, key):
        return cls.get_string(key, "").upper() in ["TRUE", "1", "YES", "Y"]
