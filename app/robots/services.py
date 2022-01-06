import secrets

from common.cache import cache
from django.conf import settings


class RobotCryptoService:
    """
    Simple service that's handle meta data about robot auth such as:
      - current counter
    """

    ACCESS_TOKEN_LENGTH = 32

    def __init__(self, robot=None):
        self._robot = robot

    def generate_access_token(self):
        access_token = secrets.token_hex(self.ACCESS_TOKEN_LENGTH)

        cache.cache_value(
            key=access_token,
            value=str(self._robot.uuid),
            expire=settings.ROBOT_ACCESS_TOKEN_TTL,
        )

        return access_token
