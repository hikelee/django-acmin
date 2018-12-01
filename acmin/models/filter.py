from collections import defaultdict

import django.apps
from django.db import models
from filelock import FileLock

from acmin.utils import attr
from .base import AcminModel
from .group import Group
from .model import Model
from .user import User

lock = FileLock("permission.lock")
lock.release(force=True)

_all_filters = defaultdict(lambda: defaultdict(list))


def get_all_filters():
    if not _all_filters:
        with lock:
            app_models = {model.__name__: model for model in django.apps.apps.get_models()}
            all_models = {model: app_models.get(model.name) for model in Model.objects.all()}
            for f in UserFilter.objects.all():
                _all_filters[f.user][all_models[f.model]].append(f)
            for f in GroupFilter.objects.all():
                for user in User.objects.filter(group=f.group).all():
                    _all_filters[user][all_models[f.model]].append(f)
    return _all_filters


class FilterValueType:
    constant = 10
    view_attribute = 5

    choices = [
        (constant, "固定值"),
        (view_attribute, "视图属性"),
    ]


class Filter(AcminModel):
    class Meta:
        abstract = True

    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    name = models.CharField("过滤器名称", max_length=100)
    value_type = models.SmallIntegerField("值类型", choices=FilterValueType.choices)
    attribute = models.CharField("属性名", max_length=100)
    value = models.CharField("属性值", max_length=500)
    enabled = models.BooleanField("开通", default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        with lock:
            _all_filters.clear()

    @classmethod
    def get_filters_dict(cls, view, user, model):
        result = {}
        for f in get_all_filters()[user][model]:
            value = f.value
            if f.value_type == FilterValueType.view_attribute:
                value = attr(view, value)
            if value is not None:
                result[f.attribute] = value
        return result

    @classmethod
    def filter(cls, query, view, model):
        if query:
            filters = cls.get_filters_dict(view, view.request.user, model)
            if filters:
                query = query.filter(**filters)
        return query


class GroupFilter(Filter):
    class Meta:
        verbose_name_plural = verbose_name = "组过滤器"

    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class UserFilter(Filter):
    class Meta:
        verbose_name_plural = verbose_name = "用户过滤器"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
