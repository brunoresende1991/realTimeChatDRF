from channels.generic.websocket import AsyncWebsocketConsumer

from django.contrib.auth.models import User

from chat.models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        if self.scope['user'].is_anonymous:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data
            }
        )

    async def chat_message(self, event):
        message = event['message']
        chat_room, _ = await ChatRoom.objects.aget_or_create(name=self.room_name)
        user = await User.objects.aget(username=self.scope['user'].username)
        await Message.objects.acreate(chatroom=chat_room, sender=user, content=message)
        await self.send(text_data=message)
