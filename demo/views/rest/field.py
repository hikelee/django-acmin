from rest_framework import serializers

from acmin.models import Field
from .base import BaseViewSet


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        # fields = '__all__'
        exclude = ('base', 'contenttype', 'python_type', 'serialize')
        depth = 0


class FieldViewSet(BaseViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
