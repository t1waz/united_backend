import pytest  # noqa

from robots.test import factories as users_factory
from users.test.conftest import *  # noqa


@pytest.fixture
def f_robot_1():
    yield users_factory.RobotFactory()
