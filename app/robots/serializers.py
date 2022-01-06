from rest_framework import serializers

from common.serializers import (
    RobotSerializerMixin,
    ValidateOnlySerializer,
)
from robots.constants import RobotCommand
from robots.models import Robot


class ReadRobotPositionSerializer(ValidateOnlySerializer):
    speed = serializers.FloatField(required=True)
    position_x = serializers.FloatField(required=True)
    position_y = serializers.FloatField(required=True)
    angle_theta = serializers.FloatField(required=True)
    datetime = serializers.DateTimeField(required=True)


class RobotCommandSerializer(RobotSerializerMixin, ValidateOnlySerializer):
    robot_uuid = serializers.CharField(required=True)
    command = serializers.CharField(required=True)

    def validate_robot_uuid(self, value):
        self._robot = self.context['user'].robots.all().filter(uuid=value).first()
        if not self._robot:
            raise serializers.ValidationError('invalid value')

        return value

    def validate_command(self, value):
        try:
            command = RobotCommand(value)
        except ValueError:
            raise serializers.ValidationError('invalid value')

        return command.value

    def validate(self, attrs):
        if not self._robot.is_command_connected:
            raise serializers.ValidationError({'robot': 'robot is not connected'})

        return attrs


class RobotLoginSerializer(RobotSerializerMixin, ValidateOnlySerializer):
    token = serializers.CharField(required=True)
    serial = serializers.CharField(required=True)

    def validate(self, attrs):
        self._robot = Robot.objects.filter(**attrs).first()
        if not self._robot:
            raise serializers.ValidationError({'data': 'invalid data'})

        return attrs
