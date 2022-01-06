import channels.layers
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.views import RobotAuthenticatedWebSocketMixin
from robots import constants
from robots.models import RobotPosition
from robots.serializers import (
    RobotCommandSerializer,
    ReadRobotPositionSerializer,
)
from robots.services import RobotCryptoService
from users.serializers import RobotLoginSerializer


class RobotObtainTokenView(APIView):
    """
    Endpoint for creating time restricted access token for robot.

    Using this token robot can authenticate itself during channel connection.
    """

    def post(self, request, *args, **kwargs):
        robot_login_serializer = RobotLoginSerializer(data=request.data)
        robot_login_serializer.is_valid(raise_exception=True)

        return Response(
            status=201,
            data={
                'access_token': RobotCryptoService(
                    robot=robot_login_serializer.robot
                ).generate_access_token()
            },
        )


class RobotCommandView(APIView):
    """
    Endpoint used to send command to robot.
    Command can be send by user who has access robot.
    """

    permission_classes = (IsAuthenticated,)

    def _send_command(self, command_data):
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'robot_command', {'type': 'send.command', **command_data}
        )

    def post(self, request, *args, **kwargs):
        robot_command_serializer = RobotCommandSerializer(
            data=request.data, context={'user': request.user}
        )
        robot_command_serializer.is_valid(raise_exception=True)

        self._send_command(command_data=robot_command_serializer.validated_data)

        return Response(status=201)


class RobotCommandChannel(RobotAuthenticatedWebSocketMixin, JsonWebsocketConsumer):
    """
    Channel for sending commands, and getting response about sended commands.
    Here robot can receive commands, and react on them.
    """

    CONNECTION_FLAG = 'is_command_connected'

    def connect(self):
        super().connect()

        async_to_sync(self.channel_layer.group_add)('robot_command', self.channel_name)

    def send_command(self, event):
        if str(self.scope['robot'].uuid) != event.get('robot_uuid'):
            return

        self.send_json(
            {
                'command': event.get('command'),
            }
        )


class RobotDataChannel(RobotAuthenticatedWebSocketMixin, JsonWebsocketConsumer):
    """
    Channel for fetching robot data and writing it to db.
    Robot should have valid auth token to establish connection.

    Each message should be JSON like with blueprint:
      {
        id: <str>
        type: <int>
        data: {
          ...
        }
      }

    Based on type we can do whatever we need.
    If success - return status ok for given id
    If failed - return status error for given id
    """

    CONNECTION_FLAG = 'is_data_connected'

    @staticmethod
    def _get_frame_type(data):
        try:
            return constants.RobotDataFrameType(data.get('type'))
        except ValueError:
            return None

    @staticmethod
    def _get_data_id(data):
        return data.get('id')

    def _handle_position_data(self, data):
        position_serializer = ReadRobotPositionSerializer(data=data)
        if not position_serializer.is_valid():
            self._return_error()

        RobotPosition.objects.create(
            **{'robot': self.scope['robot'], **position_serializer.validated_data}
        )

    def receive_json(self, content, **kwargs):
        frame_type = self._get_frame_type(data=content)

        if frame_type == constants.RobotDataFrameType.POSITION:
            self._handle_position_data(data=content.get('data'))
        # here ez extend
        else:
            self._return_error(frame_id=self._get_data_id(data=content))

        self.send_json({'status': 'ok', 'id': self._get_data_id(data=content)})
