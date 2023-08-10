import json
from django.core.management.base import BaseCommand
from chats.models import Message, Room, Thread


class Command(BaseCommand):
    help = "Populate messages with sample data"

    def add_arguments(self, parser):
        parser.add_argument("room", type=int, help="ID of the room")

    def handle(self, *args, **options):
        room_id = options["room"]
        room = Room.objects.get(id=room_id)
        thread = room.room_thread

        with open("data/sample_messages.json") as f:
            sample_messages = json.load(f)

        for conversation in sample_messages:
            message1 = Message.objects.create(
                author=thread.user1,
                room_id=room_id,
                content=conversation["message1"],
                unread=False,  # Assuming you don't want them to be marked as unread
            )

            message2 = Message.objects.create(
                author=thread.user2,
                room_id=room_id,
                content=conversation["message2"],
                unread=False,  # Assuming you don't want them to be marked as unread
            )

            # message1.replay_to = message2.id
            # message1.save()

        self.stdout.write(self.style.SUCCESS("Successfully populated messages"))
