import pytest
from channels.testing import WebsocketCommunicator

from backend.asgi import application


COMMAND_CHANNEL = '/robots/robot_command'


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_robot_cannot_connect_command_channel_without_token(f_robot_1):
    communicator = WebsocketCommunicator(application, COMMAND_CHANNEL)
    connected, _ = await communicator.connect()

    assert not connected

    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_robot_cannot_connect_command_channel_with_invalid_token(f_robot_1):
    communicator = WebsocketCommunicator(
        application, COMMAND_CHANNEL, headers={'x-token': 'invalid'}
    )
    connected, _ = await communicator.connect()

    assert not connected

    await communicator.disconnect()
