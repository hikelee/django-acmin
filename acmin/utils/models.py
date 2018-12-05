from django.db.models.fields.related import ForeignKey

from . import attr, first, memorize




@memorize
def get_model_fields(cls) -> list:
    return attr(cls, '_meta.fields')


@memorize
def get_model_fields_without_relation(model):
    fields = model._meta.fields
    result = []
    for field in fields:
        name = field.name
        if 'ForeignKey' in str(field.__class__):
            name = "%s|%s_id" % (name, name)
        result.append(name)
    return result


@memorize
def get_many_to_many_fields(cls) -> list:
    return attr(cls, '_meta.many_to_many')


def get_model_field(cls, name):
    return first([f for f in attr(cls, '_meta.fields') if f.name == name])




@memorize
def get_ancestor_attribute(child_cls, parent_cls, property_name=""):
    for name, x in get_parents(child_cls):
        name = name if not property_name else property_name + "." + name
        if x is child_cls or x is parent_cls:
            return name

        return get_ancestor_attribute(x, parent_cls, name)


@memorize
def get_ancestors(cls, max_cls=None):
    result = []
    if max_cls and not get_ancestor_attribute(cls, max_cls):
        return result
    if cls is not max_cls:
        foreign_fields = get_parents(cls)
        if foreign_fields:
            name, foreign_cls = foreign_fields[0]

            result.append((name, foreign_cls))
            if foreign_cls is not max_cls and foreign_cls is not cls:
                result += get_ancestors(foreign_cls, max_cls)
    return result


@memorize
def get_ancestors_names(cls, max_cls=None):
    return [name for (name, _) in get_ancestors(cls, max_cls)]


@memorize
def get_parents(cls) -> list:
    result = []
    for field in get_model_fields(cls):
        related_fields = attr(field, '_related_fields')
        if related_fields and isinstance(related_fields, list):
            item = related_fields[0]
            if isinstance(item, tuple):
                (i, _) = item
                if isinstance(i, ForeignKey):
                    result.append((field.name, i.related_model))
    return result
