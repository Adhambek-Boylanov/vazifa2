import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'post_{self.post_id}'

        # Guruhga ulanamiz
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Guruhdan uzilamiz
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        comment = data['comment']

        # Boshqa foydalanuvchilarga yuborish
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_comment',
                'comment': comment
            }
        )

    async def send_comment(self, event):
        comment = event['comment']

        # Brauzerga qayta yuborish
        await self.send(text_data=json.dumps({
            'comment': comment
        }))
