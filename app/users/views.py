from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import RobotLoginSerializer
from users.services import RobotCryptoService


class RobotCounterView(APIView):
    def post(self, request, *args, **kwargs):
        robot_login_serializer = RobotLoginSerializer(data=request.data)
        robot_login_serializer.is_valid(raise_exception=True)

        return Response(
            status=201,
            data={
                'counter': RobotCryptoService(
                    robot=robot_login_serializer.robot
                ).generate_counter()
            },
        )
