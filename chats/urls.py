# chat/urls.py
from django.urls import path

from . import views

app_name = 'chats'

urlpatterns = [
    path('', views.discussion_list, name='rooms'),
    path('trendings/', views.trendings, name='trendings'),
    path('invite_people/', views.invite_people, name='invite_people'),
    # path('room/<int:id>/', views.room, name='room'),
    path('discussion_room/<slug>/', views.discussion_room, name='discussion_room'),
    path('discussion_create/', views.discussion_create, name='discussion_create'),
    path('discussion_update/<int:id>/', views.discussion_update, name='discussion_update'),
    path('thread/<int:partner_id>/', views.thread, name='thread'),
    path('threads/', views.threads, name='threads'),
    path('thread_new/', views.thread_new, name='thread_new'),
    path('page_support/<int:page_id>/', views.page_support, name='page_support'),
    path('search/', views.search_room, name='search_room'),
    path('recent_rooms/', views.recent_rooms, name='recent_rooms'),
    path('chat_clear_history/', views.chat_clear_history, name='chat_clear_history'),
    path('chat_delete/', views.chat_delete, name='chat_delete'),
    path('chat_mute/', views.chat_mute, name='chat_mute'),
    path('total_unread_messages/', views.total_unread_messages, name='total_unread_messages'),
]
