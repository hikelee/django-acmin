import json
from collections import OrderedDict

from django.contrib.messages.views import SuccessMessageMixin
from django.forms import ChoiceField

from acmin.models import Permission, PermissionItem, Filter, Field
from acmin.utils import attr
from .mixins import ContextMixin, AccessMixin


class AdminFormView(SuccessMessageMixin, ContextMixin, AccessMixin):

    def post(self, request, *args, **kwargs):
        if Permission.has_permission(self.request.user, self.model, PermissionItem.savable):
            return super().post(request, *args, **kwargs)
        else:
            return self.handle_no_permission()

    def get_removed_fields(self):
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model"] = self.model
        context["model_name"] = self.model.__name__
        group_fields = Field.get_group_fields(self.request.user, self.model, contenttype=True, reverse=True)
        context["group_fields_json"] = json.dumps([[{'attribute': field.field_attribute, "class": field.field_contenttype.split(".")[1]} for field in fields] for fields in group_fields])
        self.add_foreign_field_choices(context["form"], attr(context, "object"), group_fields)
        return context

    def add_foreign_field_choices(self, form, obj, group_fields):
        choices = []
        for foreign_fields in group_fields:
            last_attribute, last_value = None, None
            for index in range(len(foreign_fields)):
                field = foreign_fields[index]
                cls = field.model
                queryset = None
                attribute = field.field_attribute
                if index == 0 or last_value:
                    queryset = cls.objects
                    filters = Filter.get_filters_dict(self, self.request.user, cls) or {}
                    if last_value:
                        filters[last_attribute[len(attribute) + 1:] + "_id"] = last_value

                    if filters:
                        queryset = queryset.filter(**filters)

                options = [(e.id, str(e)) for e in queryset.all()] if queryset else []
                # if len(options) > 1:
                options = [('', '------')] + options
                value = attr(obj, f'{attribute}_id')
                choices.append((attribute, ChoiceField(
                    required=True if form.fields.pop(attribute, False) else False,
                    initial=value,
                    label=field.verbose_name,
                    choices=options
                )))
                last_attribute = attribute
                last_value = value

        fields = OrderedDict(choices)
        fields.update(form.fields)
        form.fields = fields
