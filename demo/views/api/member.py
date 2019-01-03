from rest_framework import serializers

from demo.models import Member
from .base import BaseViewSet


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    # create_time = serializers.DateTimeField(label="加入时间", format="%Y-%m-%d %H:%M:%S", required=False, read_only=False)
    class Meta:
        model = Member
        fields = ('id', 'name')


class MemberViewSet(BaseViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
