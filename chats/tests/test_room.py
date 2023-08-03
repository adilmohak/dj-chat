"""
This test includes `RoomDetailView`, `UserRoomListView`, `InvitePeople`, 
`RoomDeleteView`, `RoomMutate`
"""

from django.test import TestCase
from django.urls import reverse
from chats.models import Room
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from chats.models import Room


class RoomTestCase(TestCase):
    def setUp(self):
        self.room = Room.objects.create(is_private=True)
        self.url = reverse("chats:room", args=[self.room.pk])

        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_room_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/room.html")
        self.assertEqual(response.context["room"], self.room)

    def test_clear_history_view(self):
        response = self.client.get(
            reverse("chats:clear_history"), {"room_id": self.room.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/partials/clear_history.html")
        # Add more tests for clearing history and redirection if needed.

    def test_room_delete_view(self):
        response = self.client.get(
            reverse("chats:room_delete", kwargs={"pk": self.room.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/partials/chat_delete.html")
        # Add more tests for deleting a room and redirection if needed.

    def test_room_mutate_view(self):
        response = self.client.post(
            reverse("chats:room_mutate"), {"room_id": self.room.id}
        )
        self.assertEqual(response.status_code, 200)
        # Add more tests for muting/unmuting a room if needed.
