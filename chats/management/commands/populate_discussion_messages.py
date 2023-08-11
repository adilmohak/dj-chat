import random
import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from chats.models import DiscussionRoom, Room, Tag, Message


user_pks = list(get_user_model().objects.all().values_list("id", flat=True))


class Command(BaseCommand):
    help = "Populate discussions with sample conversations"

    def handle(self, *args, **options):
        with open("data/sample_discussion_messages.json") as f:
            sample_messages = json.load(f)

        for message in sample_messages:
            discussions = DiscussionRoom.objects.filter(headline=message["discussion"])
            users = random.sample(user_pks, 5)
            if discussions.exists():
                d = discussions.first()
                for c in message["conversations"]:
                    Message.objects.create(
                        author_id=random.choice(users),
                        room=d.room,
                        content=c["message"],
                    )

        self.stdout.write(
            self.style.SUCCESS("Successfully populated discussion conversations")
        )
