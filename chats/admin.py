from django.contrib import admin

from .models import Room, Message, Thread, Tag, DiscussionRoom

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Thread)
admin.site.register(DiscussionRoom)
admin.site.register(Tag)
