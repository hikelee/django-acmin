from django.db import models

from .alias import Alias
from .base import AcminModel
from .contenttype import ContentType


class Field(Alias, AcminModel):
    class Meta:
        abstract = True

    contenttype = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    attribute = models.CharField("属性", max_length=100)
    list_available = models.BooleanField("列表中显示")
    form_available = models.BooleanField("表单中显示")
