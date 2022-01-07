import django.core.exceptions
import jwt
import rest_framework_simplejwt.exceptions
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenVerifySerializer

from common.utils import process_channel_headers_to_dict
from users.models import User
from users.serializers import MeSerializer


class MeView(APIView):
    """
    View used to fetch data about logged user.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response(status=200, data=MeSerializer(instance=request.user).data)


class RobotStatusChannel(JsonWebsocketConsumer):
    """
    View used by logged user to monitor robot state.
    User can only see robots that belongs to him.
    """

    JWT_USER_ID_KEY = 'user_id'
    JWT_TOKEN_KEY = 'authentication'
    ROBOT_UUID_KEY = 'robot'

    @staticmethod
    def _is_jwt_token_valid(jwt_token):
        if jwt_token is None:
            return False

        token_verify_serializer = TokenVerifySerializer(data={'token': jwt_token})

        try:
            return token_verify_serializer.is_valid()
        except rest_framework_simplejwt.exceptions.TokenError:
            return False

    @staticmethod
    def _is_robot_access(robot_uuid, user_id):
        if not robot_uuid or not user_id:
            return False

        try:
            return User.objects.filter(id=user_id, robots__uuid=robot_uuid).exists()
        except django.core.exceptions.ValidationError:
            return False

    def _get_user_id_from_jwt_token(self, jwt_token):
        jwt_data = jwt.decode(jwt_token, options={"verify_signature": False})

        return jwt_data.get(self.JWT_USER_ID_KEY)

    def connect(self):
        super().connect()

        channel_headers = process_channel_headers_to_dict(headers_data=self.scope['headers'])
        jwt_token = channel_headers.get(self.JWT_TOKEN_KEY)

        if not self._is_jwt_token_valid(jwt_token=jwt_token):
            self.close()
            return

        if not self._is_robot_access(
            robot_uuid=channel_headers.get(self.ROBOT_UUID_KEY),
            user_id=self._get_user_id_from_jwt_token(jwt_token=jwt_token),
        ):
            self.close()
            return

        self.scope['robot_uuid'] = channel_headers.get(self.ROBOT_UUID_KEY)
        async_to_sync(self.channel_layer.group_add)('robot_status', self.channel_name)

    def send_status(self, event):
        robot_uuid = event.get('robot_uuid')
        if robot_uuid and robot_uuid == self.scope['robot_uuid']:
            self.send_json(
                {
                    'state': event.get('state', ''),
                    'speed': event.get('speed', ''),
                    'position_x': event.get('position_x', ''),
                    'position_y': event.get('position_y', ''),
                }
            )
