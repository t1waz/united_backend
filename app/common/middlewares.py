from channels.db import database_sync_to_async

from common.cache import cache
from common.utils import process_channel_headers_to_dict
from robots.models import Robot


class RobotAuthMiddleware:
    ACCESS_TOKEN_HEADER = 'x-token'

    def __init__(self, app):
        self.app = app

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
            access_token=process_channel_headers_to_dict(headers_data=scope['headers']).get(
                self.ACCESS_TOKEN_HEADER
            )
        )

        return await self.app(scope, receive, send)
