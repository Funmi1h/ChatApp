import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group = f'chat_{self.conversation_id}'
        
        conv = await database_sync_to_async(Conversation.objects.get)(pk=self.conversation_id)
        participants = await database_sync_to_async(lambda: conv.participants.all())()
        if self.scope['user'] not in participants:
            return await self.close()
        
        await self.channel_layer.group_add(self.room_group, self.channel_name)
        
        await self.channel_layer.group_add(f'online_{self.conversation_id}', self.channel_name)
        await self.accept()

        
        await self.channel_layer.group_send(
            f'online_{self.conversation_id}',
            {
                'type': 'user_status',
                'user': self.scope['user'].username,
                'status': 'online'
            }
        )

    async def disconnect(self, code):
        
        await self.channel_layer.group_discard(self.room_group, self.channel_name)
        await self.channel_layer.group_discard(f'online_{self.conversation_id}', self.channel_name)

        await self.channel_layer.group_send(
            f'online_{self.conversation_id}',
            {
                'type': 'user_status',
                'user': self.scope['user'].username,
                'status': 'offline'
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get('type')

        
        if event_type == 'chat.message':
            content = data['content']
            msg = await database_sync_to_async(Message.objects.create)(
                conversation_id=self.conversation_id,
                sender=self.scope['user'],
                content=content
            )
            payload = {
                'type': 'chat.message',    
                'message_id': msg.id,
                'sender': self.scope['user'].username,
                'content': content,
                'timestamp': msg.timestamp.isoformat(),
            }
            await self.channel_layer.group_send(self.room_group, payload)

        
        elif event_type == 'typing':
            await self.channel_layer.group_send(
                self.room_group,
                {
                    'type': 'typing',      
                    'user': self.scope['user'].username,
                }
            )
        elif event_type == 'stop_typing':
            await self.channel_layer.group_send(
                self.room_group,
                {
                    'type': 'stop_typing',
                    'user': self.scope['user'].username,
                }
            )

        
        elif event_type == 'read_message':
            message_id = data['message_id']
            
            msg = await database_sync_to_async(Message.objects.get)(pk=message_id)
            await database_sync_to_async(msg.read_by.add)(self.scope['user'])
            
            await self.channel_layer.group_send(
                self.room_group,
                {
                    'type': 'message.read',
                    'message_id': message_id,
                    'user': self.scope['user'].username,
                }
            )

    

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def typing(self, event):
       
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': event['user'],
        }))

    async def stop_typing(self, event):
        await self.send(text_data=json.dumps({
            'type': 'stop_typing',
            'user': event['user'],
        }))

    async def message_read(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message.read',
            'message_id': event['message_id'],
            'user': event['user'],
        }))

    async def user_status(self, event):
       
        await self.send(text_data=json.dumps({
            'type': 'user.status',
            'user': event['user'],
            'status': event['status'],
        }))
