import random
import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from chats.models import DiscussionRoom, Room


user_pks = get_user_model().objects.all().values_list("id", flat=True)


class Command(BaseCommand):
    help = "Populate discussions with sample data"

    def handle(self, *args, **options):
        with open("data/sample_discussions.json") as f:
            sample_discussions = json.load(f)

        for discussion in sample_discussions:
            room = Room.objects.create(is_discussion=True)
            DiscussionRoom.objects.create(
                owner_id=random.choice(user_pks),
                room=room,
                headline=discussion["headline"],
                description=discussion["description"],
            )

        self.stdout.write(self.style.SUCCESS("Successfully populated discussions"))
