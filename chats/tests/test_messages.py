"""
This test includes `MessageDeleteView`, `total_unread_messages`
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from chats.models import Message, Thread, Room


class MessageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.user2 = get_user_model().objects.create_user(
            username="testuser2", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.room = Room.objects.create(is_private=True)
        self.message = Message.objects.create(
            room=self.room, author=self.user2, content="Test message"
        )

    def test_message_delete_view(self):
        response = self.client.get(
            reverse("chats:message_delete", kwargs={"pk": self.message.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/partials/message_delete.html")
        # Add more tests for deleting a message and redirection if needed.

    def test_total_unread_messages_view(self):
        # Assuming the `Thread` model has a related method `total_unread_messages` for the user
        thread = Thread.objects.create(
            room=self.room, user1=self.user2, user2=self.user
        )
        # thread.mark_message_as_unread()

        response = self.client.get(reverse("chats:total_unread_messages"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"total_unread_counter": 1})
        # Add more tests for unread message count if needed.
