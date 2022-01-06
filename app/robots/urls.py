from django.urls import path

from robots import views


app_prefix = 'robots'

urlpatterns = [
    path(
        f'{app_prefix}/robot/command', views.RobotCommandView.as_view(), name='robot_command'
    ),
    path(
        f'{app_prefix}/robot/obtain_token',
        views.RobotObtainTokenView.as_view(),
        name='robot_obtain_token',
    ),
]

websocket_urlpatterns = [
    path(
        f'{app_prefix}/robot_command',
        views.RobotCommandChannel.as_asgi(),
        name='robot_command',
    ),
    path(f'{app_prefix}/robot_data', views.RobotDataChannel.as_asgi(), name='robot_data'),
]
