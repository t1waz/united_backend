import secrets
from common.cache import cache


class RobotCryptoService:
    """
    Simple service that's handle meta data about robot auth such as:
      - current counter
    """

    COUNTER_BIT_LENGHT = 32

    def __init__(self, robot=None):
        self._robot = robot

    def generate_counter(self):
        counter = secrets.randbits(self.COUNTER_BIT_LENGHT)

        cache.cache_value(key=str(self._robot.uuid), value=counter)

        return counter
