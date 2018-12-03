from django.db import models

from .base import AcminModel
from .contenttype import ContentType
from .group import Group
from .user import User


class BaseField(AcminModel):
    class Meta:
        abstract = True

    base = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="模型")
    field_attribute = models.CharField("字段名称", max_length=100)
    field_contenttype = models.CharField(verbose_name="字段模型", max_length=100, null=True, blank=True)
    group_sequence = models.IntegerField("分组序号")
    sequence = models.IntegerField("序号")

    list_available = models.BooleanField("列表中显示", default=True)
    form_available = models.BooleanField("表单中显示", default=True)
    verbose_name = models.CharField("显示名称", max_length=200)


class Field(BaseField):
    class Meta:
        ordering = ['base', 'group_sequence', 'sequence']
        verbose_name_plural = verbose_name = "字段"
        unique_together = (("base", "field_attribute"))


class GroupField(BaseField):
    class Meta:
        ordering = ["group", 'base', 'group_sequence', 'sequence']
        verbose_name_plural = verbose_name = "字段(用户组)"
        unique_together = (("group", "base", "field_attribute"))

    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class UserField(BaseField):
    class Meta:
        ordering = ["user", 'base', 'group_sequence', 'sequence']
        verbose_name_plural = verbose_name = "字段(用户)"
        unique_together = (("user", "base", "field_attribute"))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
