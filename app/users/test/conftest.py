import pytest
from users.test import factories as users_factory


@pytest.fixture
def f_robot_1():
    yield users_factory.RobotFactory()
