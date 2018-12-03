import django.apps
from django.db import models
from filelock import FileLock

from .base import AcminModel
from .group import Group
from .user import User

lock = FileLock("contenttype.lock")
lock.release(force=True)

_model_contenttype_map = dict()
_contenttype_model_map = dict()


def _init_map():
    with lock:
        _model_contenttype_map.clear()
        _contenttype_model_map.clear()

        x = {}
        for contenttype in ContentType.objects.all():
            x[contenttype.app + "-" + contenttype.name] = contenttype

        for model in [model for model in django.apps.apps.get_models() if issubclass(model, AcminModel)]:
            app = model.__module__.split(".")[0]
            name = model.__name__
            contenttype = x[app + "-" + name]
            _model_contenttype_map[model] = contenttype
            _contenttype_model_map[contenttype] = model


def get_model_contenttype_map():
    if not _model_contenttype_map:
        _init_map()
    return _model_contenttype_map


def get_contenttype_model_map():
    if not _contenttype_model_map:
        _init_map()
    return _contenttype_model_map


class BaseContentType(AcminModel):
    class Meta:
        abstract = True

    app = models.CharField("应用", max_length=100)
    name = models.CharField("名称", max_length=100)
    verbose_name = models.CharField("描述", max_length=100)
    sequence = models.IntegerField("排序", default=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        with lock:
            _init_map()

    def __str__(self):
        return self.verbose_name


class ContentType(BaseContentType):
    class Meta:
        ordering = ['sequence']
        verbose_name_plural = verbose_name = "模型"
        unique_together = (("app", "name"))

    @classmethod
    def get_by_model(cls, model):
        return get_model_contenttype_map()[model]

    def get_model(self):
        result = get_contenttype_model_map()[self]
        return result


class GroupContentType(BaseContentType):
    class Meta:
        ordering = ['group', 'sequence']
        verbose_name_plural = verbose_name = "模型(用户组)"
        unique_together = ("group", "app", "name")

    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class UserContentType(BaseContentType):
    class Meta:
        ordering = ['user', 'sequence']
        verbose_name_plural = verbose_name = "模型(用户)"
        unique_together = ("user", "app", "name")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
