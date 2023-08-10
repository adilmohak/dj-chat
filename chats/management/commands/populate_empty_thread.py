import random
import json
from django.core.management.base import BaseCommand
from chats.models import Message, Room, Thread


class Command(BaseCommand):
    help = "Populate messages with sample data"

    def handle(self, *args, **options):
        threads = Thread.objects.filter(room__room_messages=None)

        for thread in threads:
            with open("data/sample_messages.json") as f:
                sample_messages = json.load(f)

            for conversation in random.sample(sample_messages, 6):
                message1 = Message.objects.create(
                    author=thread.user1,
                    room=thread.room,
                    content=conversation["message1"],
                    # unread=False,  # Assuming you don't want them to be marked as unread
                )

                message2 = Message.objects.create(
                    author=thread.user2,
                    room=thread.room,
                    content=conversation["message2"],
                    # unread=False,  # Assuming you don't want them to be marked as unread
                )

                # message1.replay_to = message2.id
                # message1.save()

        self.stdout.write(self.style.SUCCESS("Successfully populated messages"))
