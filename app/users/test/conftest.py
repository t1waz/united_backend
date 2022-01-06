from users.test import factories as users_factories
import pytest


@pytest.fixture
def f_active_user():
    yield users_factories.UserFactory(is_active=True)


@pytest.fixture
def f_not_active_user():
    yield users_factories.UserFactory(is_active=False)
