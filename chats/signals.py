import datetime
from django.db.models import Q
from .models import Thread, DiscussionRoom, PageSupport


def pre_save_message_handler(sender, instance, *args, **kwargs):
	instance.room.update = datetime.datetime.now()
	instance.room.save()
	if instance.room.is_discussion:
		group = DiscussionRoom.objects.filter(room=instance.room).first()
		if not instance.author in group.members.all():
			group.members.add(instance.author)
	elif instance.room.is_support:
		support = PageSupport.objects.filter(room=instance.room).first()
		if not instance.author in support.members.all():
			support.members.add(instance.author)



def pre_save_thread_receiver(sender, instance, *args, **kwargs):
	rooms = Thread.objects.filter(
		Q(user1=instance.user1, user2=instance.user2) | 
		Q(user1=instance.user2, user2=instance.user1)
	).distinct()
	if rooms.exists():
		return rooms.first()


def m2m_changed_page_support_receiver(sender, instance, *args, **kwargs):
	instance.add_members()
