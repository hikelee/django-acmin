import operator
from collections import OrderedDict
from functools import reduce

from django.db.models import Q
from django.forms import ChoiceField, forms
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views import generic
from django.views.generic.list import BaseListView

from acmin.models import Permission, PermissionItem, Filter, Field
from acmin.utils import (
    attr, get_ancestors_names, get_model_field_names
)
from acmin.utils import models as model_util
from .mixins import ContextMixin, AccessMixin


class SearchMixin(BaseListView):
    def get_toolbar_search_params(self):
        groups = model_util.get_relation_group(self.model)
        if groups:
            relation_names = [x.attribute for x in reduce(operator.add, groups)]
            return {k: v for k, v in self.request.GET.items() if k in relation_names and v}
        return {}

    def get_request_model_filters(self):
        return {k: v for k, v in self.request.GET.items() if k in get_model_field_names(self.model) and v}


class FuzzySearchMixin(BaseListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("sk")
        if keyword and len(keyword) > 0:
            search_fields = attr(self.model, "search_fields")
            if search_fields:
                q = Q()
                for field in search_fields:
                    q = q | Q(**{'%s__icontains' % field: keyword})
                queryset = queryset.filter(q)

        return queryset


class FilterForm(forms.Form):
    pass


class ToolbarSearchFormMixin(SearchMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["toolbar_search_form"] = self.get_toolbar_search_form()
        names = [x for x in get_ancestors_names(self.model)]
        context['hierarchy'] = {e: names[0:index] for index, e in enumerate(names)}
        return context

    def get_toolbar_search_form(self):
        choices = self.get_toolbar_search_fields()
        # print(choices)
        choices += self.get_toolbar_extra_search_choices()
        if choices:
            fields = OrderedDict(choices)
            form = FilterForm()
            form.fields = fields
            return form

    def get_toolbar_extra_search_choices(self):
        return []

    def get_toolbar_search_fields(self):
        choices = []
        group_fields = Field.get_group_fields(self.request.user, self.model)
        params = self.get_toolbar_search_params()
        for fields in group_fields:
            fields = [field for field in reversed(fields) if field.field_contenttype]
            last_options = None
            last_default_value = None
            for index in range(len(fields)):
                field = fields[index]
                attribute = field.field_attribute
                cls = field.model
                queryset = None
                if index == 0:
                    queryset = Filter.filter(cls.objects, self, cls)
                else:
                    last_attribute = fields[index - 1].field_attribute
                    last_value = params.get(last_attribute) or last_default_value
                    if last_value and last_options:
                        filters = {last_attribute[len(attribute) + 1:] + "_id": int(last_value)}
                        queryset = Filter.filter(cls.objects.filter(**filters), self, cls)

                options = [(e.id, str(e)) for e in queryset.all()] if queryset else []
                label = field.verbose_name
                if len(options) > 1:
                    options = [('', '选择%s' % label)] + options
                if options:
                    choices.append((attribute, ChoiceField(initial=params.get(attribute, ""), label=label, choices=options, )))

                last_default_value = options[0][0] if options else None
                last_options = options

        return choices


class OrderMixin(BaseListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get("sort")
        if sort:
            queryset = queryset.order_by(sort.replace('.', '__'))

        return queryset


class ToolbarSearchMixin(SearchMixin):
    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.get_toolbar_search_params()
        for relations in model_util.get_relation_group(self.model):
            for relation in relations:
                value = params.get(relation.attribute, None)
                if value:
                    queryset = queryset.filter(**{relation.attribute.replace(".", "__") + "_id": value})
                    break

        model_filters = self.get_request_model_filters()
        if model_filters:
            queryset = queryset.filter(**model_filters)

        sort = self.request.GET.get("sort")
        if sort:
            queryset = queryset.order_by(sort.replace('.', '__'))

        return queryset


class JsonResponseMixin(BaseListView):
    def get(self, request, *args, **kwargs):
        if self.request.GET.get("format") == 'json':
            entities = [model_to_dict(item) for item in self.get_queryset()]
            return JsonResponse(entities, safe=False)

        return super().get(request, args, kwargs)


class AdminListView(
    JsonResponseMixin,
    FuzzySearchMixin,
    ToolbarSearchFormMixin,
    ToolbarSearchMixin,
    OrderMixin,
    ContextMixin,
    AccessMixin,
    generic.ListView
):
    context_object_name = 'list'
    paginate_by = 30
    form_class = None

    def get_toolbar_search_fields(self):
        return super().get_toolbar_search_fields()

    def get_model_exclude_names(self):
        return attr(self.model, "list_exclude", [])

    def get_model_include_names(self):
        return attr(self.model, "list_fields")

    def get_model_list_fields(self):
        cls = self.model
        names = self.get_model_include_names()
        model_fields = model_util.get_model_fields(cls)
        field_dict = OrderedDict([(f.name, f) for f in model_fields])
        if names == '__all__' or not names:
            names = [f.name for f in model_fields]
        excludes = self.get_model_exclude_names()
        excludes = excludes + [
            f.name for f in model_fields if f.related_model
        ]
        result = []
        for name in names:
            verbose_name = None
            orderable = True
            if isinstance(name, tuple):
                name, verbose_name = name
                orderable = False
            if name not in excludes:
                if not verbose_name:
                    verbose_name = field_dict[name].verbose_name if name in field_dict else name
                field = model_util.Field(name, verbose_name, name, None, orderable)
                result.append(field)

        return result

    def get_relation_fields(self):
        from acmin.utils import models
        fields = [model_util.Field(relation.attribute.split(".").pop(), relation.verbose_name, relation.attribute,
                                   relation.model.__name__)
                  for relations in models.get_relation_group(self.model) for relation in relations]

        fields.reverse()
        return fields

    def get_list_fields(self):
        return self.get_relation_fields() + self.get_model_list_fields()

    def get_template_names(self):
        return [f'admin/{self.model.__name__}/list.html', 'acmin/admin/base/list.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"list_fields": self.get_list_fields()})
        for obj in context.get("list"):
            setattr(obj, "_request", self.request)

        return context

    def get_queryset(self):
        return Filter.filter(super().get_queryset(), self, self.model)

    def has_permission(self):
        return Permission.has_permission(self.request.user, self.model, PermissionItem.listable)
