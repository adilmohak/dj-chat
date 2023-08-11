import random
import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from chats.models import DiscussionRoom, Room, Tag
from django.db.utils import IntegrityError


user_pks = get_user_model().objects.all().values_list("id", flat=True)


class Command(BaseCommand):
    help = "Populate discussions with sample data"

    def handle(self, *args, **options):
        with open("data/sample_discussions.json") as f:
            sample_discussions = json.load(f)

        for discussion in sample_discussions:
            if not DiscussionRoom.objects.filter(
                headline=discussion["headline"]
            ).exists():
                room = Room.objects.create(is_discussion=True)
                new_discussion = DiscussionRoom.objects.create(
                    owner_id=random.choice(user_pks),
                    room=room,
                    headline=discussion["headline"],
                    description=discussion["description"],
                )
                tags = [Tag(name=t) for t in discussion["tags"]]
                new_tags = Tag.objects.bulk_create(tags, ignore_conflicts=True)
                new_tag_objs = [Tag.objects.get(name=t) for t in new_tags]
                new_discussion.tags.set(new_tag_objs)

        self.stdout.write(self.style.SUCCESS("Successfully populated discussions"))
