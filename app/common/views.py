class RobotAuthenticatedWebSocketMixin:
    CONNECTION_FLAG = ''

    def _return_error(self, frame_id=None):
        self.send_json({'status': 'error', 'id': frame_id})
        return

    def connect(self):
        if not self.scope.get('robot'):
            self.close()

            return

        if self.scope.get('robot'):
            setattr(self.scope['robot'], self.CONNECTION_FLAG, True)
            self.scope['robot'].save()

        super().connect()

    def disconnect(self, *args, **kwargs):
        if self.scope.get('robot'):
            setattr(self.scope['robot'], self.CONNECTION_FLAG, False)
            self.scope['robot'].save()

        super().disconnect(*args, **kwargs)
