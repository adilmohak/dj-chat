import json
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.formats import localize
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

from .models import DiscussionRoom, Message, PageSupport, Room, Thread
from .utils import send_notification, mark_messages_as_read


User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        room = get_object_or_404(Room, id=data['roomId'])
        messages = Message.objects.filter(room=data['roomId'])
        paginator = Paginator(messages, 10) # Show 10 messages per page.

        page_number = data['page']
        # Return none if the page num > total page nums
        if page_number > paginator.num_pages:
            return

        page_obj = paginator.get_page(page_number)

        next_page = page_obj.next_page_number() if page_obj.has_next() else None
        auto_scroll = False if page_obj.has_previous() else True

        # make messages unread=False
        mark_messages_as_read(page_obj.object_list, data['username'])

        # messages = get_last_10_messages(data['roomId'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(page_obj),
            'history_cleared': room.history_cleared,
            'next_page': next_page,
            'total_pages': paginator.num_pages,
            'auto_scroll': auto_scroll,
        }
        self.send_message(content)

    def new_message(self, data):
        # username = get_user(data['from'])
        user = get_object_or_404(User, email=data['from'])
        current_room = get_object_or_404(Room, id=data['roomId'])
        message = Message.objects.create(
            author=user,
            room=current_room,
            content=data['message'])
        
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        # send_notification(room_id=current_room.id, sender=user) # Send notification

        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'author': message.author.email,
            'author_uri': message.author.get_absolute_url,
            'name': message.author.get_name,
            'avatar': message.author.avatar.url,
            'content': message.content,
            'date_created': str(localize(message.created)),
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        print("WebSocket connected")

    def disconnect(self, close_code):
        id = self.room_group_name.split('_')[1]
        room = Room.objects.get(id=id)
        if not room.has_messages():
            if room.is_discussion:
                DiscussionRoom.objects.get(room=room).delete()
            elif room.is_private:
                Thread.objects.get(room=room).delete()
            elif room.is_support:
                PageSupport.objects.get(room=room).delete()

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("WebSocket closed")

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))