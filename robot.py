import asyncio
import datetime
import json
import random
import uuid

import requests
import websockets


SETTINGS = {
    'token': '',
    'serial': '',
    'robot_data_channel': 'ws://localhost:8000/robots/robot_data',
    'robot_command_channel': 'ws://localhost:8000/robots/robot_command',
    'obtain_token_url': 'http://127.0.0.1:8000/robots/robot/obtain_token',
}


def get_position_data():
    return {
        'speed': random.uniform(10.5, 175.5),
        'angle_theta': random.uniform(10.5, 180),
        'position_x': random.uniform(10.5, 275.5),
        'position_y': random.uniform(10.5, 275.5),
        'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }


class APIHandler:
    def __init__(self):
        self._token = None
        self._session = requests.Session()

    def obtain_token(self):
        self._token = None

        response = self._session.post(
            SETTINGS['obtain_token_url'],
            data={'serial': SETTINGS['serial'], 'token': SETTINGS['token']},
        )
        if response.status_code == 201:
            self._token = response.json().get('access_token')

        return self._token

    @property
    def socket_headers(self):
        return {'x-token': self._token}


async def handle_positions_data(auth_headers):
    async def _send_position_data(websocket):
        await websocket.send(
            json.dumps(
                {
                    'id': str(uuid.uuid4()),
                    'type': 1,
                    'data': get_position_data(),
                }
            )
        )

        response = await websocket.recv()
        print(response)

    async with websockets.connect(
        SETTINGS['robot_data_channel'], extra_headers=auth_headers
    ) as websocket:
        while True:
            await _send_position_data(websocket=websocket)
            await asyncio.sleep(1)


async def handle_commands(auth_headers):
    async with websockets.connect(
        SETTINGS['robot_command_channel'], extra_headers=auth_headers
    ) as websocket:
        while True:
            print('connected to commands')
            readed_command = await websocket.recv()
            print('readed command', readed_command)


if __name__ == '__main__':
    api_handler = APIHandler()
    api_handler.obtain_token()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            handle_positions_data(api_handler.socket_headers),
            handle_commands(api_handler.socket_headers),
        )
    )
