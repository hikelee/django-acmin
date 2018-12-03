from django.db import models

from .alias import Alias
from .base import AcminModel
from .group import Group
from .user import User


class ContentType(AcminModel):
    class Meta:
        ordering = ['sequence']
        verbose_name_plural = verbose_name = "模型"
        unique_together = (("app", "name"))

    app = models.CharField("应用", max_length=100)
    name = models.CharField("名称", max_length=100)
    verbose_name = models.CharField("描述", max_length=100)
    sequence = models.IntegerField("排序", default=100)

    def __str__(self):
        return f"{self.verbose_name}({self.name})"


class GroupContentType(Alias, AcminModel):
    class Meta:
        verbose_name_plural = verbose_name = "模型(用户组)"

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    contenttype = models.ForeignKey(ContentType, on_delete=models.CASCADE)


class UserContentType(Alias, AcminModel):
    class Meta:
        verbose_name_plural = verbose_name = "模型(用户)"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contenttype = models.ForeignKey(ContentType, on_delete=models.CASCADE)
