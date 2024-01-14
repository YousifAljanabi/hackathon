import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class PartyConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        type = data["type"]

        if type == "chat_message":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    "type": "chat_message",
                    "message": data['message'],
                    "from": data['from'],
                    "time": data['time'],
                }
            )
            # Send message to db

        if type == "video_state":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    "type": "video_state",
                    "state": data['state'],
                }
            )

        if type == "time_sync":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    "type": "time_sync",
                    "time": data['time'],
                }
            )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
                "message": event["message"],
                "from": event["from"],
                "type": "chat_message",
                "time": event["time"],
            }))

    def video_state(self, event):
        self.send(text_data=json.dumps({
                "state": event["state"],
                "type": "video_state",
            }))

    def time_sync(self, event):
        self.send(text_data=json.dumps({
                "time": event["time"],
                "type": "time_sync",
            }))