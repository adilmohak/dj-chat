"""
This test includes `MessageDeleteView`, `total_unread_messages`
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from chats.models import Message, Thread


class MessageDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.message = Message.objects.create(author=self.user, content="Test message")

    def test_message_delete_view(self):
        response = self.client.get(
            reverse("chats:delete_message", kwargs={"pk": self.message.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/partials/message_delete.html")
        # Add more tests for deleting a message and redirection if needed.

    def test_total_unread_messages_view(self):
        # Assuming the `Thread` model has a related method `total_unread_messages` for the user
        thread = Thread.objects.create(user1=self.user, user2=self.user)
        thread.mark_message_as_unread()

        response = self.client.get(reverse("chats:total_unread_messages"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"total_unread_counter": 1})
        # Add more tests for unread message count if needed.
