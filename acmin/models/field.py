from collections import defaultdict

from django.db import models
from filelock import FileLock

from .base import AcminModel
from .contenttype import ContentType
from .group import Group
from .user import User

_user_model_fields = defaultdict(lambda: defaultdict(list))

lock = FileLock("field.lock")
lock.release(force=True)


def update_content_type(field):
    if field.field_contenttype:
        app, name = field.field_contenttype.split(".")
        field.field_contenttype = ContentType.objects.filter(app=app, name=name).first()


def get_all_fields():
    if not _user_model_fields:
        with lock:
            for field in GroupField.objects.all():
                update_content_type(field)
                model = field.base.get_model()
                for user in User.objects.filter(group=field.group).all():
                    _user_model_fields[user][model].append(field)

            for field in UserField.objects.all():
                update_content_type(field)
                model = field.base.get_model()
                _user_model_fields[user][model].append(field)

            for field in Field.objects.all():
                update_content_type(field)
                model = field.base.get_model()
                for user in User.objects.all():
                    _user_model_fields[user][model].append(field)

            for user, model_map in _user_model_fields.items():
                for model, _ in model_map.items():
                    _user_model_fields[user][model].sort(key=lambda f: (f.group_sequence, f.sequence))

    return _user_model_fields


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

    @classmethod
    def get_fields(cls, user, model):
        return get_all_fields()[user][model]

    @classmethod
    def get_group_fields(cls, user, model):
        result = []
        group_sequence = -1
        fields = []
        for field in cls.get_fields(user, model):
            if group_sequence != field.group_sequence:
                group_sequence = field.group_sequence
                if fields:
                    result.append(fields)
                fields = []
            fields.append(field)
        if fields:
            result.append(fields)
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
