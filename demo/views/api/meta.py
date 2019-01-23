import collections

from acmin.models import Field, ContentType, Choice
from acmin.router import api_route
from acmin.serializer import BaseSerializer
from acmin.utils import param


class FieldSerializer(BaseSerializer):
    class Meta:
        model = Field
        exclude = ('base', 'python_type', 'serialize')
        depth = 1


# http://127.0.0.1:7000/api/demo/meta/?model=Member
@api_route("api/demo/meta/")
def get_meta(request):
    contenttype: ContentType = ContentType.get("demo", param(request, "model"))
    if contenttype:
        fields = Field.get_fields(request.user, contenttype.get_model())
        choices = collections.defaultdict(collections.OrderedDict)
        for field in fields:
            for choice in Choice.get_choices(field):
                choices[field.attribute][choice.value] = choice.title
        return dict(
            status=200,
            message="success",
            data=dict(
                type=dict(label=contenttype.verbose_name, name=contenttype.name),
                fields=[FieldSerializer(field).data for field in fields],
                choices=choices,
            )
        )

    return dict(status=1)
