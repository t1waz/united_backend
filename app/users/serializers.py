from rest_framework import serializers

from common.serializers import (
    RobotSerializerMixin,
    ValidateOnlySerializer,
)
from robots.models import Robot


class RobotLoginSerializer(RobotSerializerMixin, ValidateOnlySerializer):
    token = serializers.CharField(required=True)
    serial = serializers.CharField(required=True)

    def validate(self, attrs):
        self._robot = Robot.objects.filter(**attrs).first()
        if not self._robot:
            raise serializers.ValidationError({'data': 'invalid data'})

        return attrs
