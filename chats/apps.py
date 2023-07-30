from django.apps import AppConfig


class ChatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chats"

    def ready(self) -> None:
        from django.db.models.signals import pre_save, post_save
        from .models import Thread, Message
        from .signals import (
            pre_save_message_handler,
            pre_save_thread_receiver,
        )

        pre_save.connect(pre_save_message_handler, sender=Message)
        pre_save.connect(pre_save_thread_receiver, sender=Thread)

        return super().ready()
