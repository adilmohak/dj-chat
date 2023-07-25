# chat/urls.py
from django.urls import path

from . import views

app_name = "chats"

urlpatterns = [
    path("", views.DiscussionListView.as_view(), name="rooms"),
    path(
        "discussion_room/<slug>/",
        views.DiscussionDetailView.as_view(),
        name="discussion_room",
    ),
    path("trendings/", views.Trendings.as_view(), name="trendings"),
    path("invite_people/", views.InvitePeople.as_view(), name="invite_people"),
    # path('room/<int:id>/', views.room, name='room'),
    path(
        "discussion_create/",
        views.DiscussionFormView.as_view(),
        name="discussion_create",
    ),
    path(
        "discussion_update/<int:pk>/",
        views.DiscussionUpdateView.as_view(),
        name="discussion_update",
    ),
    path("thread/<str:pk>/", views.ThreadDetailView.as_view(), name="thread"),
    path("threads/", views.ThreadListView.as_view(), name="threads"),
    path("thread_new/", views.ThreadCreateView.as_view(), name="thread_new"),
    path("chat_mute/", views.RoomMutate.as_view(), name="chat_mute"),
    path(
        "chat_clear_history/", views.ClearHistory.as_view(), name="chat_clear_history"
    ),
    path("chat_delete/<int:pk>/", views.RoomDeleteView.as_view(), name="chat_delete"),
    path("search/", views.DiscussionSearchView.as_view(), name="search_room"),
    path("user_rooms/", views.UserRoomListView.as_view(), name="user_rooms"),
    path(
        "total_unread_messages/",
        views.total_unread_messages,
        name="total_unread_messages",
    ),
]
