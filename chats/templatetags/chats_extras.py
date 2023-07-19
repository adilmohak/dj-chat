from django import template
from django.db.models import Q
from chats.models import Message

register = template.Library()

@register.simple_tag
def get_partner(current_user, room, *args, **kwargs):
	user = room.user1 if current_user == room.user2 else room.user2
	return user


@register.simple_tag
def is_unread(msg, user, *args, **kwargs):
	if msg is not None:
		if msg.author == user:
			return False
		return msg.unread


@register.simple_tag
def unread_count(room, user):
	"""Count of unread messages"""
	return room.unread_count(user=user)
