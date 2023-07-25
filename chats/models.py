import datetime
import json
import re
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.views import get_user_model
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from autoslug import AutoSlugField


class RoomManager(models.Manager):
    def total_unread_messages(self):
        unread_count = 0
        rooms = self.model.objects.filter(is_private=True)
        for room in rooms:
            unread_count += room.unread_count()
        return unread_count


class Room(TimeStampedModel):
    """This is the model where all chats (thread, discussion, support) gonna use"""

    # Track whether the room should be intended to act like a private chat
    # one-to-one chat
    is_private = models.BooleanField(default=False)

    # Track whether the room should be intended to act like a support chat
    # support chat is a group chat where acceble only for the page admins
    # and the chat initiator/customer
    is_support = models.BooleanField(default=False)

    # Track whether the room should be intended to act like a discussion chat
    # a discussion chat is a group chat where acceble by any user
    is_discussion = models.BooleanField(default=False)

    # Notifications associated to the room won't be created
    # for the users who set the room to `mute=True`.
    muted = models.BooleanField(default=False)

    # Track if the room history has been cleared
    # used for displaying `History cleared` message
    history_cleared = models.BooleanField(default=False)

    # Count connected clients/users
    # Useful for displaying online users
    connected_clients = models.ManyToManyField(settings.AUTH_USER_MODEL)

    objects = RoomManager()

    class Meta:
        ordering = ("-modified", "id")

    @property
    def get_absolute_url(self):
        return reverse("chats:room", kwargs={"id": self.id})

    def connect(self, user):
        """Add connected user to `connected_clients`"""
        if not user in self.connected_clients:
            self.connected_clients.add(user)

    def disconnect(self, user):
        """Remove connected user from `connected_clients`"""
        if user in self.connected_clients:
            self.connected_clients.remove(user)

    def has_messages(self):
        """check whether the room has messages"""
        # return Message.objects.filter(room=self).exists()
        return self.room_messages.exists()

    def unread_messages(self, user):
        """Unread messages means: `unread=True` and `not created by us`"""
        return self.room_messages.filter(Q(unread=True) & ~Q(author=user))

    def unread_count(self, user):
        """Count of unread messages"""
        # return self.room_messages.filter(Q(room=self, unread=True) & ~Q(author=user)).count()
        return self.unread_messages(user).count()

    def get_messages(self):
        """All messages of the room ever created"""
        # messages = self.room_messages.filter(room=self)
        return self.room_messages.all()

    def latest_message(self):
        """The latest message created with this room if it exists, otherwise return `None`"""
        if self.has_messages():
            # return self.room_messages.filter(room=self).latest('created')
            return self.room_messages.latest("created")
        return

    def latest_messages_count(self, days_limit=30):
        """Latest messages of the room, messages that are newer or equal with `days_limit`.
        This is used for sorting rooms by trendings(highest messages within some period of time)
        """
        time_limit = datetime.datetime.now() - datetime.timedelta(days=days_limit)
        messages = self.room_messages.filter(created__gte=time_limit).count()

        return messages

    def snip_room_members(self, limit=3):
        """Return `limit` number of distinct users that has been created messages inside the room.
        Used for rendering snip users pic"""
        # TODO: Try to use another method instead of `distinct` since it requires
        # to be the same as initial order_by
        messages = (
            self.room_messages.all().order_by("author").distinct("author")[:limit]
        )
        return [m.author for m in messages]

    def members(self):
        """Return all members of the room by extracting messages"""
        return self.room_messages.all().order_by("author_id").distinct("author")

    def clear_chat_history(self):
        """
        clear/delete every message associated to this room and return deleted
        messages count for later reference, and set room as `history_cleared=True`
        """
        msgs = self.room_messages.all()
        msgs_count = msgs.count()
        msgs.delete()
        self.history_cleared = True
        self.save()
        return msgs_count


class Message(models.Model):
    # Store replaying message id or leave null if the user didn't replay to
    # any message
    replay_to = models.IntegerField(blank=True, null=True)

    # author is a user who created the message
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # a room this message associated with
    room = models.ForeignKey(
        Room, related_name="room_messages", on_delete=models.CASCADE
    )

    # content is the actual message written
    content = models.TextField(null=True)

    # Track whether the user has been readed the message or not
    # usefull for displaying notifications and able the user
    # to know the message is not been readed yet
    unread = models.BooleanField(default=True)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.content

    @property
    def replay_msg(self):
        if self.replay_to:
            replaying_msg = self.objects.filter(id=self.replay_to).first()
            if replaying_msg:
                return replaying_msg
        return


class ThreadManager(models.Manager):
    def new_or_get(self, current_user, partner):
        qs = self.get_queryset().filter(
            Q(user1=current_user, user2=partner) | Q(user1=partner, user2=current_user)
        )
        if qs.count() == 1:
            created = False
            chat_obj = qs.first()
        else:
            room = Room.objects.create(is_private=True)
            chat_obj = Thread.objects.new(room=room, user1=current_user, user2=partner)
            created = True
        return chat_obj, created

    def new(self, room, user1, user2):
        # room = Room.objects.create(owner=current_user)
        new_chat = self.model.objects.create(room=room, user1=user1, user2=user2)
        return new_chat

    def total_unread_messages(self, user):
        unread_count = 0
        threads = self.model.objects.filter(Q(user1=user) | Q(user2=user)).distinct()
        for t in threads:
            unread_count += t.room.unread_count(user)
        return unread_count

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = Q(user1__name__icontains=query) | Q(
                user2__name__icontains=query
            )
            qs = qs.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Thread(models.Model):
    """Thread is a private chat which only two users can join the room"""

    # Override the default id, which is bigint to a uuid field
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # a room which this thread associated with
    # thread is a OneToOneField relation to room to make sure one
    # thread can have only one room
    room = models.OneToOneField(Room, on_delete=models.CASCADE)

    # Since this is a one-on-one chat, we only store two users
    # First user
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="chat_thread_first",
        on_delete=models.SET_NULL,
    )

    # Second user
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="chat_thread_second",
        on_delete=models.SET_NULL,
    )

    objects = ThreadManager()

    class Meta:
        # doesn't allow to create multiple threads with same users
        # because it doesn't make sense
        unique_together = ["user1", "user2"]
        ordering = ("-room__modified",)

    def __str__(self):
        return f"{self.user1} - {self.user2}"

    def get_all_messages(self):
        msgs = Message.objects.filter(room=self.room).values()
        return msgs

    def get_partner(self, request):
        """Return the other user(not the current user) in the room,
        if the current user is user1, then the partner is user2 or vise versa"""
        return self.user1 if request.user == self.user2 else self.user2


class Tag(models.Model):
    # we only need to store the name of the tag
    # name will be used for searching purpose and
    # describing the object associated with the tag
    name = models.CharField(max_length=124, unique=True)

    def __str__(self):
        return self.name


class DiscussionRoomManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(headline__icontains=query)
                | Q(description__icontains=query)
                | Q(messages_dump__icontains=query)
            )
            qs = qs.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return qs

    def get_trendings(self, qs=None):
        """rooms that has more recent(one month range) updates/messages
        are considered as a highest trending."""
        # TODO: instead of just comparing with amount of created messages,
        # also compare with how many users created the messages
        if qs == None:
            qs = DiscussionRoom.objects.all()
        one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
        recent_rooms = qs.filter(modified__gte=one_month_ago).order_by("-modified")
        trendings = recent_rooms.order_by("room__latest_messages_count")
        return trendings


class DiscussionRoom(models.Model):
    # owner is a user who created the room
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    # OneToOneField to ensure that one room can have only one discussion room
    room = models.OneToOneField(Room, on_delete=models.CASCADE)

    # headline is the main idea or topic about the discussion.
    # all members should be discussed on ideas that are related to the topic
    # we keep this field unique to minimize duplication of ideas as much as we can
    headline = models.CharField(max_length=220, unique=True)

    # Optional field which describes the headline further
    description = models.TextField(null=True, blank=True)

    class DiscussionMode(models.TextChoices):
        NEUTRAL = "NE", _("Neutral")
        HAPPY = "HA", _("Happy")
        SAD = "SA", _("Sad")
        CELEBRATION = "CE", _("Celebration")
        BUSINESS = "BU", _("Business")
        CODING = "CO", _("Coding")

    # mode describes what the discussion feeling should be, it's depend on
    # the headline of the discussion. For example, if the discussion is
    # about celebration, then the mode should be `Happy`
    # and accordingly the mode, the UI of discussion also changes
    mode = models.CharField(
        max_length=2, choices=DiscussionMode.choices, default=DiscussionMode.NEUTRAL
    )

    # As soon as the user creates a message with this room, he/she will be added to
    # members list
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="discussion_members", blank=True
    )

    # User can add tags to the discussion so that the group will recommend to others that
    # has already joined another group with same tags
    # and also discussions can search over tags
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        help_text="Add tags related to the topic, use dash(-) instead of space.",
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # user friendly url display generated from the headline
    slug = AutoSlugField(
        populate_from="headline", unique=True
    )  # generate slug from headline

    # for searching purpose, all contents of every message in this discussion stores here
    messages_dump = models.TextField(null=True, blank=True)

    objects = DiscussionRoomManager()

    def __str__(self):
        return f"{self.owner} - {self.headline}"

    @property
    def get_absolute_url(self):
        return reverse("chats:discussion_room", kwargs={"slug": self.slug})

    def set_messages_dump(self):
        """Set all message contents in one text. can be run every two days. Helps for searching"""
        msgs = list(Message.objects.filter(room=self.room).values_list("content"))
        if msgs:
            # 1. join all tuples inside list,
            # 2. join all list to one str,
            # 3. replace new line with space,
            # 4. replace multiple spaces with single space
            self.messages_dump = re.sub(
                " +", " ", (" ".join([i for m in msgs for i in m]).replace("\n", " "))
            )
            self.save()


# class PageSupportManager(models.Manager):
#     def new_or_get(self, user, page):
#         qs = self.get_queryset().filter(members=user, page=page)
#         if qs.count() == 1:
#             created = False
#             chat_obj = qs.first()
#         else:
#             room = Room.objects.create(is_support=True)
#             chat_obj = PageSupport.objects.new(room=room, user=user, page=page)
#             created = True
#         return chat_obj, created

#     def new(self, room, user, page):
#         new_chat = self.model.objects.create(room=room, user=user, page=page)
#         return new_chat


# class PageSupport(models.Model):
#     # we can't make UUID because the model containes manytomany field
#     # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     # user is who initiates the support room, if the users deletes, then we don't need
#     # to store data associated to the support group
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="initiator"
#     )

#     # Since this is a support room we need to store the page(Collection)
#     # page = models.ForeignKey('book_collections.Collection', on_delete=models.CASCADE)

#     # OneToOneField to ensure that one room can have only one support group
#     room = models.OneToOneField(Room, on_delete=models.CASCADE)

#     # members will be only page admins and the room initiator, more particularly the `user`
#     members = models.ManyToManyField(
#         settings.AUTH_USER_MODEL, related_name="group_members", blank=True
#     )

#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)

#     objects = PageSupportManager()

#     def __str__(self):
#         return f"{self.user}"

#     def add_members(self):
#         """This will add page admins who has permission to access chats and the initiator"""
#         admins = self.page.admins().values("user")
#         admin_users = set(get_user_model().objects.filter(id__in=admins))
#         admin_users.add(self.user)
#         admin_users.add(self.page.user)
#         self.members.set(admin_users)


# class UnreadMessages(models.Model):
# 	"""This model has a role to count unread messages for a specific user and room"""
# 	pass
