from collections import defaultdict

from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from filelock import FileLock

from acmin.utils import first, attr
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
    if sender in [Group, User, Field, UserField, GroupField]:
        with lock:
            cache.clear()


def get_all_fields():
    if not cache:
        with lock:
            temp_cache = defaultdict(lambda: defaultdict(dict))
            for field in Field.objects.all():
                model = field.base.get_model()
                for user in User.objects.all():
                    temp_cache[user][model][field.attribute] = field

            base_attributes = ['sequence', 'listable', 'formable', 'sortable', 'exportable', 'verbose_name']
            for group_field in GroupField.objects.all():
                field = group_field.field
                model = field.base.get_model()
                for user in User.objects.filter(group=group_field.group).all():
                    default_field = temp_cache[user][model][field.attribute]
                    for attribute in base_attributes:
                        setattr(default_field, attribute, getattr(group_field, attribute))

            for user_field in UserField.objects.all():
                field = user_field.field
                model = field.base.get_model()
                default_field = temp_cache[user][model][field.attribute]
                for attribute in base_attributes:
                    setattr(default_field, attribute, getattr(user_field, attribute))

            for user, model_map in temp_cache.items():
                for model, field_dict in model_map.items():
                    cache[user][model] = sorted(field_dict.values(), key=lambda f: (f.group_sequence, f.sequence))

    return cache


class BaseField(AcminModel):
    class Meta:
        abstract = True

    sequence = models.IntegerField("序号")
    listable = models.BooleanField("在列表中显示", default=True)
    formable = models.BooleanField("在表单中显示", default=True)
    sortable = models.BooleanField("可排序", default=True)
    exportable = models.BooleanField("可导出", default=True)
    nullable = models.BooleanField("可以为空", default=False)
    unique = models.BooleanField("是否唯一性", default=False)
    default = models.CharField("默认值", max_length=500, null=True, blank=True)
    verbose_name = models.CharField("显示名称", max_length=200)


class Field(BaseField):
    class Meta:
        ordering = ['base', 'group_sequence', 'sequence']
        verbose_name_plural = verbose_name = "字段"
        # unique_together = (("base", "attribute"))

    base = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="模型", related_name="base")
    attribute = models.CharField("字段名称", max_length=100)
    contenttype = models.ForeignKey(ContentType, verbose_name="字段模型", null=True, blank=True, on_delete=models.CASCADE, related_name="contenttype")
    group_sequence = models.IntegerField("分组序号")
    python_type = models.CharField("原生类型", max_length=200)

    def __str__(self):
        return f"{self.base},{self.verbose_name}({self.attribute})"

    @classmethod
    def get_field(cls, user, model, attribute):
        return first([field for field in get_all_fields()[user][model] if field.attribute == attribute])

    @classmethod
    def get_fields(cls, user, model):
        return get_all_fields()[user][model]

    @property
    def model(self):
        if self.contenttype:
            return self.contenttype.get_model()

    @property
    def class_name(self):
        return attr(self.model, "__name__")

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
            if field.contenttype or not contenttype:
                fields.append(field)
        if fields:
            result.append(list(reversed(fields)) if reverse else fields)
        return result


class GroupField(BaseField):
    class Meta:
        ordering = ["group", 'field']
        verbose_name_plural = verbose_name = "字段(用户组)"
        unique_together = [("group", "field")]

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, verbose_name="默认字段")

    def __str__(self):
        return f"{self.group},{self.verbose_name}({self.field.attribute})"


class UserField(BaseField):
    class Meta:
        ordering = ["user", 'field']
        verbose_name_plural = verbose_name = "字段(用户)"
        unique_together = [("user", "field")]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user},{self.verbose_name}({self.field.attribute})"
