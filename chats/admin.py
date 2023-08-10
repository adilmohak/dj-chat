from django.contrib import admin

from .models import Room, Message, Thread, Tag, DiscussionRoom


class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "is_private",
        "is_discussion",
        "history_cleared",
        "created",
        "modified",
    ]


admin.site.register(Room, RoomAdmin)
admin.site.register(Message)
admin.site.register(Thread)
admin.site.register(DiscussionRoom)
admin.site.register(Tag)
