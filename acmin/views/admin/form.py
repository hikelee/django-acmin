from collections import OrderedDict

from django.contrib.messages.views import SuccessMessageMixin
from django.forms import ChoiceField

from acmin.models import Permission, PermissionItem, Filter
from acmin.utils import attr, get_ancestor_attribute, get_ancestors, get_ancestors_names
from .mixins import  ContextMixin, AccessMixin


class AdminFormView(SuccessMessageMixin,  ContextMixin, AccessMixin):

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
        context["ancestors"] = self.get_ancestor_attribute_variables()
        context["model"] = self.model
        context["model_name"] = self.model.__name__

        return context

    def get_ancestor_attribute_variables(self):
        cls = self.model
        ancestors = list(reversed(get_ancestors(cls)))
        length = len(ancestors)

        def to_dict(chain):
            name, cls = chain
            return dict(
                name=name,
                class_name=cls.__name__,
                filters=Filter.get_filters_dict(self, self.request.user, cls)
            )

        result = [dict(
            name=name,
            child=to_dict(ancestors[index + 1]),
            offsprings=[to_dict(c) for c in ancestors[index + 1:length]]
        ) for index, (name, cls) in enumerate(ancestors[0:length - 1])]
        return result

    def _add_relation_choices(self, context):
        obj = attr(context, "object")
        form = context["form"]
        choices = []

        chain_names = get_ancestors_names(self.model)
        length = len(chain_names)
        chains = get_ancestors(self.model)
        removed_fields = self.get_removed_fields()
        for index, (attribute, cls) in enumerate(chains):
            if attribute not in removed_fields:
                queryset = cls.objects
                filters = Filter.get_filters_dict(self, self.request.user, cls)
                if filters:
                    queryset = queryset.filter(**filters)

                obj = attr(obj, attribute)
                if obj and index < length - 1:
                    parent_attribute_name = chain_names[index + 1]
                    parent_id = attr(obj, parent_attribute_name + ".id")
                    if parent_id:
                        f = {parent_attribute_name + "_id": parent_id}
                        queryset = queryset.filter(**f)
                else:
                    for c, f in filters:
                        relation = get_ancestor_attribute(cls, c)
                        if relation:
                            f = {relation.replace(".", "__") + "__" + key: value for key, value in f.items()}
                            queryset = queryset.filter(**f)

                options = [(e.id, str(e)) for e in queryset.all()]
                if len(options) > 1:
                    options = [('', '-----')] + options
                choices.append((attribute, ChoiceField(
                    required=True if form.fields.pop(attribute, False) else False,
                    initial=attr(obj, "id"),
                    label=attr(cls, '_meta.verbose_name'),
                    choices=options
                )))
        choices.reverse()

        fields = OrderedDict(choices)
        fields.update(form.fields)
        for f in removed_fields:
            fields.pop(f, None)
        form.fields = fields
