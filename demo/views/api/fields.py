import collections

from django.contrib.auth.decorators import login_required
from rest_framework import serializers

from acmin.models import Field, ContentType, Choice
from acmin.utils import param, json_response
from acmin.views import route
from .base import BaseViewSet


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        # fields = '__all__'
        exclude = ('base', 'python_type', 'serialize')
        depth = 1


class FieldViewSet(BaseViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer


# http://127.0.0.1:8000/api/demo/meta/?type=Member
@route("api/demo/fields/")
@login_required
def get_meta(request):
    contenttype: ContentType = ContentType.get("demo", param(request, "type"))
    if contenttype:
        fields = Field.get_fields(request.user, contenttype.get_model())
        choices = collections.defaultdict(collections.OrderedDict)
        for field in fields:
            for choice in Choice.get_choices(field):
                choices[field.attribute][choice.value] = choice.title
        return json_response(dict(
            status=0,
            type=dict(verbose_name=contenttype.verbose_name, name=contenttype.name),
            fields=[FieldSerializer(field).data for field in fields],
            choices=choices,
        ))

    return json_response(dict(status=1))
