from rest_framework import serializers


class ValidateOnlySerializer(serializers.Serializer):
    def create(self, *args, **kwargs):
        raise ValueError('not used')

    def update(self, *args, **kwargs):
        raise ValueError('not used')


class RobotSerializerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._robot = None

    @property
    def robot(self):
        if not hasattr(self, '_validated_data'):
            raise AssertionError(
                'You must call `.is_valid()` before accessing robot attribute'
            )

        return self._robot
