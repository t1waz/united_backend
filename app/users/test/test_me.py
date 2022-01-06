import pytest
from django.urls import reverse
from rest_framework.test import APIClient

api_client = APIClient()


@pytest.mark.django_db
class TestMeView:
    URL_NAME = 'me_view'

    def test_get_request_on_robot_command_view_not_logged(self):
        response = api_client.get(path=reverse(self.URL_NAME))

        assert response.status_code == 401

    def test_patch_request_on_robot_command_view_not_logged(self):
        response = api_client.patch(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 401

    def test_put_request_on_robot_command_view_not_logged(self):
        response = api_client.put(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 401

    def test_delete_request_on_robot_command_view_not_logged(self):
        response = api_client.put(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 401

    def test_patch_request_on_robot_command_view_logged(self, f_active_user):
        api_client.force_authenticate(user=f_active_user)
        response = api_client.patch(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

    def test_put_request_on_robot_command_view_logged(self, f_active_user):
        api_client.force_authenticate(user=f_active_user)
        response = api_client.put(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

    def test_delete_request_on_robot_command_view_logged(self, f_active_user):
        api_client.force_authenticate(user=f_active_user)
        response = api_client.put(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

