import django.apps
from django.db.models import ForeignKey

from acmin.utils import attr


def init_contenttype():
    from acmin.models import ContentType, AcminModel
    contenttypes = {}
    for contenttype in ContentType.objects.all():
        contenttypes[contenttype.app + "-" + contenttype.name] = contenttype
    models = {}
    for model in [model for model in django.apps.apps.get_models() if issubclass(model, AcminModel)]:
        app = model.__module__.split(".")[0]
        name = model.__name__
        models[app + "-" + name] = model

    type_map = {}
    for flag, model in models.items():
        contenttype = contenttypes.get(flag)
        verbose_name = model._meta.verbose_name
        if contenttype:
            if contenttype.verbose_name != verbose_name:
                contenttype.verbose_name = verbose_name
                contenttype.save()
        else:
            app, name = flag.split("-")
            contenttype = ContentType.objects.create(app=app, name=name, verbose_name=verbose_name)
        type_map[model] = contenttype
    for flag, contenttype in contenttypes.items():
        if flag not in models:
            contenttype.delete()

    return type_map


def init_fields(type_map):
    from acmin.models import AcminModel, Field
    new = []
    for model in django.apps.apps.get_models():
        if issubclass(model, AcminModel):
            group_sequence = 100
            base = type_map.get(model)
            attributes = []

            fields = [field for field in attr(model, '_meta.fields') if not attr(field, "remote_field")]
            for sequence, field in enumerate(fields, start=1):
                name, verbose_name = attr(field, "name"), attr(field, '_verbose_name')
                attributes.append(name)
                if not Field.objects.filter(base=base, field_attribute=name).first():
                    new.append(Field(
                        base=base,
                        field_attribute=name,
                        group_sequence=group_sequence,
                        sequence=sequence,
                        verbose_name=verbose_name
                    ))
            for group_sequence, relations in enumerate(get_relation_group(model), start=1):
                for sequence, relation in enumerate(relations, start=1):
                    contenttype = type_map.get(relation.model)
                    attributes.append(relation.attribute)
                    if not Field.objects.filter(base=base, field_attribute=relation.attribute).first():
                        new.append(Field(
                            base=base,
                            field_contenttype=f"{contenttype.app}.{contenttype.name}",
                            field_attribute=relation.attribute,
                            group_sequence=group_sequence,
                            sequence=sequence,
                            verbose_name=relation.verbose_name
                        ))

            Field.objects.filter(base=base).exclude(field_attribute__in=attributes).delete()
    Field.objects.bulk_create(new)


def init_models(sender, **kwargs):
    type_map = init_contenttype()
    init_fields(type_map)


def get_relation_group(model):
    class Relation(object):
        def __init__(self, model, attribute, verbose_name):
            self.model = model
            self.attribute = attribute
            self.verbose_name = verbose_name

        def __repr__(self):
            return f"({self.model},{self.attribute},{self.verbose_name})"

    def get_relation1(cls):
        relations = []
        fields = attr(cls, '_meta.fields')
        for field in fields:
            remote_field = attr(field, "remote_field")
            if remote_field:
                related_model = attr(remote_field, "model")
                field = attr(remote_field, "field")
                if issubclass(type(field), ForeignKey):
                    relations.append((related_model, attr(field, "name")))
        return relations

    def _get_attributes(cls, name=None):
        relations = get_relation1(cls)
        names = []
        for relation_model, relation_attribute in relations:
            new_name = f"{name}.{relation_attribute}" if name else relation_attribute
            new_names = _get_attributes(relation_model, new_name)
            if new_names:
                names += new_names
            else:
                names.append(new_name)

        return names

    group, relations = [], []
    last_attribute = None

    attributes = _get_attributes(model)

    for attribute in attributes:
        names = attribute.split(".")
        for i in range(1, len(names) + 1):
            sub_attribute, cls, verbose_name = ".".join(
                names[0:i]), model, None
            for name in sub_attribute.split("."):
                field = attr(cls, f"{name}.field")
                verbose_name = attr(field, "_verbose_name")
                cls = attr(field, f"remote_field.model")
            if not verbose_name:
                verbose_name = attr(cls, "_meta.verbose_name")
            relation = Relation(cls, sub_attribute, verbose_name)
            if not relations or sub_attribute.startswith(last_attribute):
                relations.append(relation)
            elif relations:
                group.append(relations)
                relations = [relation]
            last_attribute = sub_attribute

    if relations:
        group.append(relations)
    return group
