from rest_framework import serializers

from robots.models import Robot
from users.models import User


class MeSerializer(serializers.ModelSerializer):
    robots = serializers.SlugRelatedField(
        many=True, queryset=Robot.objects.all(), slug_field='uuid'
    )

    class Meta:
        model = User
        fields = ('uuid', 'first_name', 'last_name', 'is_active', 'robots')
