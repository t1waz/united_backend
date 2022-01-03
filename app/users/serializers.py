from rest_framework import serializers
from users.models import Robot


class RobotLoginSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    serial = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._robot = None

    def validate(self, attrs):
        self._robot = Robot.objects.filter(**attrs).first()
        if not self._robot:
            raise serializers.ValidationError({'data': 'invalid data'})

        return attrs

    def create(self, *args, **kwargs):
        raise ValueError('not used')

    def update(self, *args, **kwargs):
        raise ValueError('not used')

    @property
    def robot(self):
        if not hasattr(self, '_validated_data'):
            raise AssertionError(
                'You must call `.is_valid()` before accessing robot attribute'
            )

        return self._robot
