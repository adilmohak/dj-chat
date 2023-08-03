"""
This test includes `DiscussionDetailView`, `DiscussionListView`, `DiscussionFormView`, 
`DiscussionUpdateView`, `DiscussionSearchView`
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from chats.models import DiscussionRoom
from chats.forms import InviteForm


class DiscussionDetailViewTestCase(TestCase):
    def setUp(self):
        self.client.login(username="testuser", password="testpassword")
        self.discussion_room = DiscussionRoom.objects.create(name="Test Discussion")
        self.detail_url = reverse("discussion-detail", args=[self.discussion_room.pk])

        for i in range(20):
            room = DiscussionRoom.objects.create(name=f"Discussion {i}")
            room.members.add(self.user)
        self.list_url = reverse("discussion-list")

        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.user_rooms_url = reverse("user-rooms")

        self.trendings_url = reverse("trendings")

        self.room = DiscussionRoom.objects.first()
        self.invite_url = reverse("invite-people")
        self.form_data = {
            "room": self.room.pk,
            "users": [1, 2, 3],  # Assuming user ids 1, 2, 3 are valid
        }

    def test_discussion_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/discussion_detail.html")
        self.assertEqual(response.context["room"], self.discussion_room)

    def test_discussion_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/discussions.html")
        self.assertEqual(len(response.context["rooms"]), 16)  # paginate_by is 16

    def test_user_room_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/partials/user_rooms.html")
        self.assertEqual(len(response.context["rooms"]), 10)  # paginate_by is 10

    def test_trendings_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/trendings.html")
        self.assertEqual(len(response.context["discussions"]), 3)  # paginate_by is 3

    def test_invite_people_view(self):
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("Invitation sent!", response.content.decode())
        self.assertInHTML(
            "Your invitation has been sent to [username1, username2, username3]",
            response.content.decode(),
        )
