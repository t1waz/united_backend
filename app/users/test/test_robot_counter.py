import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from common.cache import cache


api_client = APIClient()


@pytest.mark.django_db
class TestRobotCounterView:
    URL_NAME = 'robot_counter'

    def test_get_request_on_robot_counter_view(self):
        response = api_client.get(path=reverse(self.URL_NAME))

        assert response.status_code == 405

    def test_patch_request_on_robot_counter_view(self):
        response = api_client.patch(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

    def test_put_request_on_robot_counter_view(self):
        response = api_client.put(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

    def test_delete_request_on_robot_counter_view(self):
        response = api_client.delete(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 405

    def test_post_request_on_robot_counter_view_empty_payload(self):
        response = api_client.post(path=reverse(self.URL_NAME), data={})

        assert response.status_code == 400
        assert set(response.data.keys()) == {'token', 'serial'}

    def test_post_request_on_robot_counter_view_missing_serial(self, f_robot_1):
        response = api_client.post(
            path=reverse(self.URL_NAME), data={'token': f_robot_1.token}
        )

        assert response.status_code == 400
        assert 'serial' in response.data

    def test_post_request_on_robot_counter_view_missing_token(self, f_robot_1):
        response = api_client.post(
            path=reverse(self.URL_NAME), data={'serial': f_robot_1.serial}
        )

        assert response.status_code == 400
        assert 'token' in response.data

    def test_post_request_on_robot_counter_view_invalid_serial(self, f_robot_1):
        response = api_client.post(
            path=reverse(self.URL_NAME),
            data={'serial': 'some_invalid_serial', 'token': f_robot_1.token},
        )

        assert response.status_code == 400
        assert 'data' in response.data

    def test_post_request_on_robot_counter_view_invalid_token(self, f_robot_1):
        response = api_client.post(
            path=reverse(self.URL_NAME),
            data={'serial': f_robot_1.serial, 'token': 'invalid_token'},
        )

        assert response.status_code == 400
        assert 'data' in response.data

    def test_post_request_on_robot_counter_view_valid_data(self, f_robot_1):
        response = api_client.post(
            path=reverse(self.URL_NAME),
            data={'serial': f_robot_1.serial, 'token': f_robot_1.token},
        )

        assert response.status_code == 201
        assert 'counter' in response.data

    def tet_post_request_on_robot_counter_view_valid_data_created_cached_counter(
        self, f_robot_1
    ):
        response = api_client.post(
            path=reverse(self.URL_NAME),
            data={'serial': f_robot_1.serial, 'token': f_robot_1.token},
        )

        assert response.status_code == 201
        assert cache.get_value(key=str(f_robot_1.uuid)) == response.data['counter']
