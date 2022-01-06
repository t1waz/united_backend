import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch
from asgiref.sync import async_to_sync


api_client = APIClient()


@pytest.mark.django_db
class TestRobotCounterView:
    URL_NAME = 'robot_command'

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
        response = api_client.delete(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 401

    def test_get_request_on_robot_command_view_logged_as_active_user(self, f_active_user):
        api_client.force_authenticate(user=f_active_user)
        response = api_client.get(path=reverse(self.URL_NAME))

        assert response.status_code == 405

    def test_patch_request_on_robot_command_view_logged_as_active_user(self, f_active_user):
        api_client.force_authenticate(user=f_active_user)
        response = api_client.patch(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

    def test_put_request_on_robot_command_view_logged_as_active_user(self, f_active_user):
        api_client.force_authenticate(user=f_active_user)
        response = api_client.put(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

    def test_delete_request_on_robot_command_view_logged_as_active_user(self, f_active_user):
        api_client.force_authenticate(user=f_active_user)
        response = api_client.delete(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

    def test_get_request_on_robot_command_view_logged_as_not_active_user(
        self, f_not_active_user
    ):
        api_client.force_authenticate(user=f_not_active_user)
        response = api_client.get(path=reverse(self.URL_NAME))

        assert response.status_code == 405

    def test_patch_request_on_robot_command_view_logged_as_not_active_user(
        self, f_not_active_user
    ):
        api_client.force_authenticate(user=f_not_active_user)
        response = api_client.patch(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

    def test_put_request_on_robot_command_view_logged_as_not_active_user(
        self, f_not_active_user
    ):
        api_client.force_authenticate(user=f_not_active_user)
        response = api_client.put(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

    def test_delete_request_on_robot_command_view_logged_as_not_active_user(
        self, f_not_active_user
    ):
        api_client.force_authenticate(user=f_not_active_user)
        response = api_client.delete(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

    def test_post_request_on_robot_command_view_missing_robot_uuid(self, f_active_user):
        api_client.force_authenticate(user=f_active_user)
        response = api_client.post(path=reverse(self.URL_NAME), data={'command': 'auto'})

        assert response.status_code == 400
        assert 'robot_uuid' in response.data

    def test_post_request_on_robot_command_view_missing_command(
        self, f_active_user, f_robot_1
    ):
        f_active_user.robots.add(f_robot_1)
        f_active_user.save()

        api_client.force_authenticate(user=f_active_user)
        response = api_client.post(path=reverse(self.URL_NAME), data={'robot_uuid': f_robot_1})

        assert response.status_code == 400
        assert 'command' in response.data

    def test_post_request_on_robot_command_view_invalid_command(
        self, f_active_user, f_robot_1
    ):
        f_active_user.robots.add(f_robot_1)
        f_active_user.save()

        api_client.force_authenticate(user=f_active_user)
        response = api_client.post(
            path=reverse(self.URL_NAME),
            data={'robot_uuid': str(f_robot_1.uuid), 'command': 'invalid'},
        )

        assert response.status_code == 400
        assert 'command' in response.data

        response = api_client.post(
            path=reverse(self.URL_NAME),
            data={'robot_uuid': str(f_robot_1.uuid), 'command': 123},
        )

        assert response.status_code == 400
        assert 'command' in response.data

        response = api_client.post(
            path=reverse(self.URL_NAME),
            data={'robot_uuid': str(f_robot_1.uuid), 'command': 3.14},
        )

        assert response.status_code == 400
        assert 'command' in response.data

        response = api_client.post(
            path=reverse(self.URL_NAME),
            data={'robot_uuid': str(f_robot_1.uuid), 'command': False},
        )

        assert response.status_code == 400
        assert 'command' in response.data

    def test_post_request_on_robot_command_view_invalid_robot_uuid(self, f_active_user):
        api_client.force_authenticate(user=f_active_user)
        response = api_client.post(
            path=reverse(self.URL_NAME), data={'robot_uuid': 'invalid', 'command': 'auto'}
        )

        assert response.status_code == 400
        assert 'robot_uuid' in response.data

        response = api_client.post(
            path=reverse(self.URL_NAME), data={'robot_uuid': 123, 'command': 'auto'}
        )

        assert response.status_code == 400
        assert 'robot_uuid' in response.data

        response = api_client.post(
            path=reverse(self.URL_NAME), data={'robot_uuid': 3.14, 'command': 'auto'}
        )

        assert response.status_code == 400
        assert 'robot_uuid' in response.data

        response = api_client.post(
            path=reverse(self.URL_NAME), data={'robot_uuid': False, 'command': 'auto'}
        )

        assert response.status_code == 400
        assert 'robot_uuid' in response.data

    def test_post_request_on_robot_command_view_robot_that_not_belongs_to_user(
        self, f_active_user, f_robot_1
    ):
        api_client.force_authenticate(user=f_active_user)
        response = api_client.post(
            path=reverse(self.URL_NAME),
            data={'robot_uuid': str(f_robot_1.uuid), 'command': 'auto'},
        )

        assert response.status_code == 400
        assert 'robot_uuid' in response.data

    def test_post_request_on_robot_command_view_robot_not_connected(
        self, f_active_user, f_robot_1
    ):
        f_active_user.robots.add(f_robot_1)
        f_active_user.save()

        f_robot_1.is_command_connected = False
        f_robot_1.save()

        api_client.force_authenticate(user=f_active_user)
        response = api_client.post(
            path=reverse(self.URL_NAME),
            data={'robot_uuid': str(f_robot_1.uuid), 'command': 'auto'},
        )

        assert response.status_code == 400
        assert 'robot' in response.data

    def test_post_request_on_robot_command_view_robot_connected(
        self, mocker, f_active_user, f_robot_1
    ):
        mocked_layer_call = mocker.patch('robots.views.RobotCommandView._send_command')

        f_active_user.robots.add(f_robot_1)
        f_active_user.save()

        f_robot_1.is_command_connected = True
        f_robot_1.save()

        api_client.force_authenticate(user=f_active_user)
        response = api_client.post(
            path=reverse(self.URL_NAME),
            data={'robot_uuid': str(f_robot_1.uuid), 'command': 'auto'},
        )

        assert response.status_code == 201
        mocked_layer_call.assert_called()
