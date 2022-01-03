import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    robots = models.ManyToManyField('users.Robot', related_name='robots')

    def __str__(self):
        return self.email


class Robot(models.Model):
    serial = models.CharField(max_length=255, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.serial
