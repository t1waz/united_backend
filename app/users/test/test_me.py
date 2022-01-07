import pytest  # noqa
from django.urls import reverse
from rest_framework.test import APIClient

from robots.test.conftest import *  # noqa


api_client = APIClient()


@pytest.mark.django_db
class TestMeView:
    URL_NAME = 'me_view'

    def test_get_request_on_me_view_not_logged(self):
        response = api_client.get(path=reverse(self.URL_NAME))

        assert response.status_code == 401

    def test_patch_request_on_me_view_not_logged(self):
        response = api_client.patch(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 401

    def test_put_request_on_me_view_not_logged(self):
        response = api_client.put(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 401

    def test_delete_request_on_me_view_not_logged(self):
        response = api_client.put(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 401

    def test_patch_request_on_me_view_logged(self, f_active_user):
        api_client.force_authenticate(user=f_active_user)
        response = api_client.patch(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

    def test_put_request_on_me_view_logged(self, f_active_user):
        api_client.force_authenticate(user=f_active_user)
        response = api_client.put(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

    def test_delete_request_on_me_view_logged(self, f_active_user):
        api_client.force_authenticate(user=f_active_user)
        response = api_client.put(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

    def test_get_request_on_me_view_logged(self, f_active_user, f_robot_1):
        f_active_user.robots.add(f_robot_1)
        f_active_user.save()

        api_client.force_authenticate(user=f_active_user)
        response = api_client.get(path=reverse(self.URL_NAME))

        assert response.status_code == 200

        assert response.data.get('uuid') == str(f_active_user.uuid)
        assert response.data.get('first_name') == f_active_user.first_name
        assert response.data.get('last_name') == f_active_user.last_name
        assert response.data.get('is_active') == f_active_user.is_active
        assert response.data.get('robots') == [f_robot_1.uuid]
