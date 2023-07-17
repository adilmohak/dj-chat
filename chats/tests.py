from django.test import TestCase

from django.urls import reverse
from django.contrib.auth import get_user_model

# from accounts.models import BusinessPage
from .models import Room, Thread, DiscussionRoom, PageSupport


class ChatsTests(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="test1@example.com", password="testing321"
        )
        self.user2 = get_user_model().objects.create_user(
            username="test2@example.com", password="testing321"
        )
        room_for_thread = Room.objects.create(is_private=True)
        room_for_discussion = Room.objects.create(is_discussion=True)

        self.thread = Thread.objects.create(
            room=room_for_thread, user1=self.user1, user2=self.user2
        )
        self.d_room = DiscussionRoom.objects.create(
            headline="Test Discussion", room=room_for_discussion, owner=self.user1
        )
        # self.page = BusinessPage.objects.create(user=self.user1, name="Test page")
        # self.support_group, created = PageSupport.objects.new_or_get(self.user1, page)

        self.client.login(username="test1@example.com", password="testing321")

    def test_discussion_room_detail_page(self):
        response = self.client.get(
            reverse("chats:discussion_room", kwargs={"slug": self.d_room.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="chats/discussion_room.html")

    def test_discussion_list_page(self):
        # self.client.login(username="test1@example.com", password="testing321")
        response = self.client.get(reverse("chats:rooms"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="chats/discussions.html")

    def test_thread_detail_page(self):
        # self.client.login(username="test1@example.com", password="testing321")
        response = self.client.get(
            reverse("chats:thread", kwargs={"partner_id": self.user1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="chats/thread_single.html")

    def test_threads_page(self):
        # self.client.login(username="test1@example.com", password="testing321")
        response = self.client.get(reverse("chats:threads"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="chats/threads.html")

    def test_thread_detail_page(self):
        # self.client.login(username="test1@example.com", password="testing321")
        response = self.client.get(
            reverse("chats:thread", kwargs={"partner_id": self.user1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="chats/thread_single.html")

    def test_thread_new_page(self):
        # self.client.login(username="test1@example.com", password="testing321")
        response = self.client.get(reverse("chats:thread_new"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="chats/thread_new.html")

    def test_page_support_page(self):
        # self.client.login(username="test1@example.com", password="testing321")
        response = self.client.get(
            reverse("chats:page_support", kwargs={"page_id": self.page.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name="chats/page_support_single.html"
        )

    def test_discussion_create_page(self):
        # self.client.login(username="test1@example.com", password="testing321")
        response = self.client.get(reverse("chats:discussion_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name="chats/discussion_room_form.html"
        )

    def test_discussion_update_page(self):
        # self.client.login(username="test1@example.com", password="testing321")
        response = self.client.get(
            reverse("chats:discussion_update", kwargs={"id": self.d_room.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name="chats/discussion_room_form.html"
        )

    def test_recent_discussions_page(self):
        # self.client.login(username="test1@example.com", password="testing321")
        response = self.client.get(reverse("chats:recent_rooms"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name="chats/partials/recent_rooms_popup.html"
        )

    def test_discussion_search_room_page(self):
        # self.client.login(username="test1@example.com", password="testing321")
        response = self.client.get(reverse("chats:search_room") + "?q=random")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="chats/search_room.html")

    def test_discussion_invite_page(self):
        # self.client.login(username="test1@example.com", password="testing321")
        response = self.client.get(reverse("chats:invite_people"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="chats/invite.html")

    def test_discussion_trendings_page(self):
        # self.client.login(username="test1@example.com", password="testing321")
        response = self.client.get(reverse("chats:trendings"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="chats/trendings.html")
