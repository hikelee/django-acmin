import collections

import django.apps
from django.db import models
from filelock import FileLock

from acmin.utils import attr
from .base import AcminModel
from .group import Group
from .contenttype import AcminContentType
from .user import User

_all_permissions = collections.defaultdict(dict)

lock = FileLock("permission.lock")
lock.release(force=True)


def _get_permissions():
    if not _all_permissions:
        with lock:
            app_models = {model.__name__: model for model in django.apps.apps.get_models()}
            all_models = {model: app_models.get(model.name) for model in AcminContentType.objects.all()}

            for user in User.objects.all():
                for model, app_model in all_models.items():
                    _all_permissions[user][app_model] = UserPermission(user=user, model=model)

            for permission in GroupPermission.objects.all():
                for user in User.objects.filter(group=permission.group):
                    _all_permissions[user][all_models[permission.model]] = permission
            for permission in UserPermission.objects.all():
                _all_permissions[permission.user][all_models[permission.model]] = permission

            for permission in GroupPermission.objects.filter(model__name=SuperPermissionModel.__name__):
                for user in User.objects.filter(group=permission.group):
                    for model, app_model in all_models.items():
                        _all_permissions[user][app_model] = permission

            for permission in UserPermission.objects.filter(model__name=SuperPermissionModel.__name__):
                for model, app_model in all_models.items():
                    _all_permissions[permission.user][app_model] = permission

    return _all_permissions


class ModelPermission:
    def __init__(self, **kwargs):
        self.removable = kwargs.get("removable")
        self.cloneable = kwargs.get("cloneable")
        self.viewable = kwargs.get("viewable")
        self.savable = kwargs.get("savable")

    @property
    def operable(self):
        return self.viewable or self.removable or self.cloneable


class PermissionItem:
    creatable = "creatable"
    savable = "savable"
    removable = "removable"
    cloneable = "cloneable"
    exportable = "exportable"
    viewable = "viewable"
    listable = "listable"


VALID_ITEMS = set([key for key, _ in vars(PermissionItem).items() if not key.startswith("_")])


class Permission(AcminModel):
    class Meta:
        abstract = True

    model = models.ForeignKey(AcminContentType, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=100)
    creatable = models.BooleanField("可创建", default=False)
    savable = models.BooleanField("可保存", default=False)
    removable = models.BooleanField("可删除", default=False)
    cloneable = models.BooleanField("可复制", default=False)
    exportable = models.BooleanField("可导出", default=False)
    viewable = models.BooleanField("可查看", default=False)
    listable = models.BooleanField("可列表", default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        with lock:
            _all_permissions.clear()

    def to_instance_permission(self):
        return ModelPermission(
            removable=self.removable,
            cloneable=self.cloneable,
            viewable=self.viewable,
            savable=self.savable
        )

    def __str__(self):
        return self.name

    @property
    def operable(self):
        return self.viewable or self.removable or self.cloneable

    @classmethod
    def get_permission(cls, user, model):
        return _get_permissions()[user][model]

    @classmethod
    def has_permission(cls, user, model, item):
        if item in VALID_ITEMS:
            return attr(cls.get_permission(user, model), item)


class GroupPermission(Permission):
    class Meta:
        verbose_name_plural = verbose_name = "用户组权限"
        unique_together = (('group', 'model'),)

    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class UserPermission(Permission):
    class Meta:
        verbose_name_plural = verbose_name = "用户权限"
        unique_together = (('user', 'model'),)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SuperPermissionModel(AcminModel):
    """
    代表所有模型，一般用在admin用户组/用户下
    """

    class Meta:
        verbose_name_plural = verbose_name = "超級模型"
