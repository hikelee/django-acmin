from django.db import models

from .alias import Alias
from .base import AcminModel
from .contenttype import ContentType
from .group import Group
from .user import User


class Field(Alias, AcminModel):
    class Meta:
        abstract = True

    contenttype = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    attribute = models.CharField("属性", max_length=100)
    list_available = models.BooleanField("列表中显示", default=True)
    form_available = models.BooleanField("表单中显示", default=True)


class GroupFiled(Field):
    class Meta:
        verbose_name_plural = verbose_name = "字段(用户组)"

    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class UserFiled(Field):
    class Meta:
        verbose_name_plural = verbose_name = "字段(用户)"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
