import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class RelayStateConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = "relay_updates"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()
        print('WebSocket connection established.')

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        print('WebSocket connection closed.')

    # Receive message from room group
    def relay_state_update(self, event):
        mac_addr = event["mac_addr"]
        state = event["state"]
        if mac_addr and state: print('Received message from client:', mac_addr, state)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "mac_addr": mac_addr,
            "state": state
        }))
        print('Sent message to client:', mac_addr, state)
