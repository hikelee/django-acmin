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
        self._add_relation_choices(context)

        context["model"] = self.model
        context["model_name"] = self.model.__name__

        return context

    def _add_relation_choices(self, context):
        user = self.request.user
        obj = attr(context, "object")
        form = context["form"]
        choices = []
        group_fields = Field.get_group_fields(user, self.model, contenttype=True, reverse=True)
        context["group_fields"] = group_fields
        group_array = []

        for foreign_fields in group_fields:
            json_array = []
            group_array.append(json_array)
            last_attribute, last_value = None, None
            for index in range(len(foreign_fields)):
                field = foreign_fields[index]
                cls = field.model
                queryset = cls.objects
                attribute = field.field_attribute
                json_array.append({"attribute": attribute, "class": cls.__name__})
                filters = Filter.get_filters_dict(self, self.request.user, cls) or {}
                if last_attribute and last_value:
                    filters[last_attribute[len(attribute) + 1:] + "_id"] = last_value

                if filters:
                    queryset = queryset.filter(**filters)

                options = [(e.id, str(e)) for e in queryset.all()]
                if len(options) > 1:
                    options = [('', '-----')] + options
                choices.append((attribute, ChoiceField(
                    required=True if form.fields.pop(attribute, False) else False,
                    initial=attr(obj, "id"),
                    label=field.verbose_name,
                    choices=options
                )))
                last_attribute = attribute
                last_value = attr(obj, 'id')

        fields = OrderedDict(choices)
        fields.update(form.fields)
        form.fields = fields
        context["group_fields_json"] = json.dumps(group_array)
