import uuid

from django.db import models


class Robot(models.Model):
    serial = models.CharField(max_length=255, unique=True)
    is_data_connected = models.BooleanField(default=False)
    is_command_connected = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.serial


class RobotPosition(models.Model):
    speed = models.FloatField(null=True, blank=True)
    position_x = models.FloatField(null=True, blank=True)
    position_y = models.FloatField(null=True, blank=True)
    angle_theta = models.FloatField(null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    robot = models.ForeignKey(
        'robots.Robot', related_name='positions', on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.created_at} {self.speed}'
