from django.db import models

from .base import AcminModel
from .group import Group
from .model import Model
from .user import User


class FilterValueType:
    constant = 10
    view_attribute = 5

    choices = [
        (constant, "固定值"),
        (view_attribute, "视图属性"),
    ]


class BaseFilter(AcminModel):
    class Meta:
        abstract = True

    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    name = models.CharField("过滤器名称", max_length=100)
    value_type = models.SmallIntegerField("值类型", choices=FilterValueType.choices)
    attribute = models.CharField("属性名", max_length=100)
    value = models.CharField("属性值", max_length=500)
    enabled = models.BooleanField("开通", default=True)


class GroupFilter(BaseFilter):
    class Meta:
        verbose_name_plural = verbose_name = "组过滤器"

    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class UserFilter(BaseFilter):
    class Meta:
        verbose_name_plural = verbose_name = "用户过滤器"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
