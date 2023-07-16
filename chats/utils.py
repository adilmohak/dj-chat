from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import get_user_model
from .models import Room, Message, DiscussionRoom

User = get_user_model()


# def get_last_10_messages(roomId):
# 	"""Returns latest 10 messages of specific room"""
# 	room = get_object_or_404(Room, id=roomId)
# 	messages = reversed(Message.objects.order_by('-created').filter(room=room)[:10])
# 	return messages


# from notifications.models import *
# from notifications.api.serializers import NotificationSerializer
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q


# def send_notification(type, room_id=None, sender=None):
# 	room = Room.objects.get(id=room_id)
# 	# discussion_room = DiscussionRoom.objects.get(room=room)
# 	# comment = post.comments.create(user=request.user, content=request.POST.get('content'))
# 	notification = CustomNotification.objects.create(type="discussion", recipient=room.owner, actor=sender, verb="New message on your discussion room", redirect_url=room.get_absolute_url)
# 	channel_layer = get_channel_layer()
# 	channel = "discussion_notifications_{}".format(room.owner.id)
# 	print(json.dumps(NotificationSerializer(notification).data))
# 	async_to_sync(channel_layer.group_send)(
# 		channel, {
# 			"type": "notify",
# 			"command": "new_discussion_notification",
# 			"notification": json.dumps(NotificationSerializer(notification).data)
# 		}
# 	)
# 	print("Notification sent")
# 	return JsonResponse({"SENT": "Notification sent"})


def mark_messages_as_read(messages, username):
    user = User.objects.get(email=username)
    for msg in messages:
        # check if the msg is created by current user and it is unread
        if not msg.author == user and msg.unread:
            msg.unread = False
            msg.save()
