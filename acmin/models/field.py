from collections import defaultdict

from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from filelock import FileLock

from .base import AcminModel
from .contenttype import ContentType
from .group import Group
from .user import User

cache = defaultdict(lambda: defaultdict(list))

lock = FileLock("field.lock")
lock.release(force=True)


@receiver(post_save)
@receiver(post_delete)
def handle_model_change(sender, **kwargs):
    if sender in [Group, User] or issubclass(sender, BaseField):
        with lock:
            cache.clear()


def get_all_fields():
    if not cache:
        with lock:
            for field in GroupField.objects.all():
                model = field.base.get_model()
                for user in User.objects.filter(group=field.group).all():
                    cache[user][model].append(field)

            for field in UserField.objects.all():
                model = field.base.get_model()
                cache[user][model].append(field)

            for field in Field.objects.all():
                model = field.base.get_model()
                for user in User.objects.all():
                    cache[user][model].append(field)

            for user, model_map in cache.items():
                for model, _ in model_map.items():
                    cache[user][model].sort(key=lambda f: (f.group_sequence, f.sequence))

    return cache


class BaseField(AcminModel):
    class Meta:
        abstract = True

    base = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="模型")
    field_attribute = models.CharField("字段名称", max_length=100)
    field_contenttype = models.CharField(verbose_name="字段模型", max_length=100, null=True, blank=True)
    group_sequence = models.IntegerField("分组序号")
    sequence = models.IntegerField("序号")

    listable = models.BooleanField("在列表中显示", default=True)
    formable = models.BooleanField("在表单中显示", default=True)
    sortable = models.BooleanField("可排序", default=True)
    exportable = models.BooleanField("可导出", default=True)

    verbose_name = models.CharField("显示名称", max_length=200)

    @classmethod
    def get_fields(cls, user, model):
        return get_all_fields()[user][model]

    @property
    def contenttype(self):
        if self.field_contenttype:
            return ContentType.get_by_key(self.field_contenttype)

    @property
    def model(self):
        if self.field_contenttype:
            return ContentType.get_model_by_key(self.field_contenttype)

    @classmethod
    def get_group_fields(cls, user, model, contenttype=False, reverse=False):
        result = []
        group_sequence = -1
        fields = []
        for field in cls.get_fields(user, model):
            if group_sequence != field.group_sequence:
                group_sequence = field.group_sequence
                if fields:
                    result.append(list(reversed(fields)) if reverse else fields)
                fields = []
            if field.field_contenttype or not contenttype:
                fields.append(field)
        if fields:
            result.append(list(reversed(fields)) if reverse else fields)
        return result

    def __str__(self):
        return self.field_attribute


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
