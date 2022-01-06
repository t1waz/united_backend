from common.cache import cache
from robots.models import Robot
from channels.db import database_sync_to_async


class RobotAuthMiddleware:
    ACCESS_TOKEN_HEADER = 'x-token'

    def __init__(self, app):
        self.app = app

    @staticmethod
    def _process_headers_to_dict(headers_data):
        if isinstance(headers_data, dict):
            return headers_data

        try:
            return {data[0].decode(): data[1].decode() for data in headers_data}
        except (ValueError, AttributeError):
            return {data[0]: data[1] for data in headers_data}

    @database_sync_to_async
    def _get_robot_by_uuid(self, robot_uuid):
        return Robot.objects.filter(uuid=robot_uuid).first()

    async def _get_robot_for_access_token(self, access_token):
        if not access_token:
            return None

        robot_uuid = cache.get_value(key=access_token)
        if not robot_uuid:
            return None

        return await self._get_robot_by_uuid(robot_uuid=robot_uuid)

    async def __call__(self, scope, receive, send):
        scope['robot'] = await self._get_robot_for_access_token(
            access_token=self._process_headers_to_dict(headers_data=scope['headers']).get(
                self.ACCESS_TOKEN_HEADER
            )
        )

        return await self.app(scope, receive, send)
