from django.db import models

from .base import AcminModel
from .group import Group
from .model import Model
from .user import User


class PermissionItem:
    creatable = "creatable"
    savable = "savable"
    removable = "removable"
    cloneable = "cloneable"
    exportable = "exportable"
    viewable = "viewable"
    listable = "listable"


VALID_ITEMS = set([key for key, _ in vars(PermissionItem).items() if not key.startswith("_")])


class BasePermission(AcminModel):
    class Meta:
        abstract = True

    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=100)
    creatable = models.BooleanField("可创建", default=True)
    savable = models.BooleanField("可保存", default=True)
    removable = models.BooleanField("可删除", default=True)
    cloneable = models.BooleanField("可复制", default=True)
    exportable = models.BooleanField("可导出", default=True)
    viewable = models.BooleanField("可查看", default=True)
    listable = models.BooleanField("可列表", default=True)
    enabled = models.BooleanField("开通", default=True)

    @property
    def operable(self):
        return self.viewable or self.removable or self.cloneable

    @staticmethod
    def has_permission(user, model, item):
        if item in VALID_ITEMS:
            group_filters = {
                'group__user': user,
                'model__name__in': [model.__name__, SuperPermissionModel.__name__],
                item: True
            }
            user_filters = {
                'user': user,
                'model__name__in': [model.__name__, SuperPermissionModel.__name__],
                item: True
            }
            if GroupPermission.objects.filter(**group_filters).first() or UserPermission.objects.filter(
                    **user_filters).first():
                return True


class GroupPermission(BasePermission):
    class Meta:
        verbose_name_plural = verbose_name = "用户组权限"

    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class UserPermission(BasePermission):
    class Meta:
        verbose_name_plural = verbose_name = "用户权限"

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SuperPermissionModel(AcminModel):
    """
    代表所有模型，一般用在admin用户组/用户下
    """

    class Meta:
        verbose_name_plural = verbose_name = "所用模型"