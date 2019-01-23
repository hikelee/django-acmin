import logging

from demo.models import Member
from .base import BaseViewSet, BaseSerializer

logger = logging.getLogger(__name__)


class MemberSerializer(BaseSerializer):
    class Meta:
        model = Member


class MemberViewSet(BaseViewSet):
    class Meta:
        model = Member


