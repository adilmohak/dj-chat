"""
This test includes `ThreadListView`, `ThreadDetailView`, `ThreadCreateView`, `ClearHistory`
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from chats.models import Thread, Room


class ThreadTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.room = Room.objects.create(is_private=True)
        self.thread = Thread.objects.create(
            room=self.room, user1=self.user, user2=self.user2
        )

    def test_thread_list_view(self):
        response = self.client.get(reverse("chats:threads"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/threads.html")
        # self.assertContains(response, "List of threads")
        # Add more tests for the context data and queryset if needed.

    def test_thread_detail_view(self):
        response = self.client.get(
            reverse("chats:thread", kwargs={"pk": self.thread.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/thread_single.html")
        # self.assertContains(response, "Thread details")
        # Add more tests for the context data and thread details if needed.

    def test_thread_create_view(self):
        response = self.client.get(reverse("chats:thread_new"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/thread_new.html")

        # Test form submission with valid data
        data = {"recipients": [self.user.id], "message": "Test message"}
        response = self.client.post(reverse("chats:thread_new"), data)
        self.assertEqual(response.status_code, 200)
        # Add more tests for successful form submission and validation if needed.
