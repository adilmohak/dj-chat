from django.apps import AppConfig


class ChatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chats'

    def ready(self) -> None:
        from django.db.models.signals import pre_save, post_save
        from .models import Thread, Message, PageSupport
        from .signals import pre_save_message_handler, pre_save_thread_receiver, m2m_changed_page_support_receiver

        pre_save.connect(pre_save_message_handler, sender=Message)
        pre_save.connect(pre_save_thread_receiver, sender=Thread)
        post_save.connect(m2m_changed_page_support_receiver, sender=PageSupport)

        return super().ready()
