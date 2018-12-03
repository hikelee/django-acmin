from django.db import models

from .alias import Alias
from .base import AcminModel
from .group import Group
from .user import User


class ContentType(AcminModel):
    class Meta:
        verbose_name_plural = verbose_name = "模型"

    name = models.CharField("名称", max_length=100, unique=True)
    verbose_name = models.CharField("描述", max_length=100)

    def __str__(self):
        return f"{self.verbose_name}({self.name})"


class ContentTypeAlias(Alias):
    class Meta:
        abstract = True

    contenttype = models.ForeignKey(ContentType, on_delete=models.CASCADE)


class GroupContentTypeAlias(ContentTypeAlias):
    class Meta:
        verbose_name_plural = verbose_name = "模型别名(用户组)"

    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class UserContentTypeAlias(ContentTypeAlias):
    class Meta:
        verbose_name_plural = verbose_name = "模型别名(用户)"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
