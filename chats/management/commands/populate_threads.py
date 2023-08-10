import random
import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from chats.models import Thread, Room
from django.db.models import Q

user_pks = get_user_model().objects.all().values_list("id", flat=True)


class Command(BaseCommand):
    help = "Populate threads with sample data"

    def handle(self, *args, **options):
        for i in range(6):
            room = Room.objects.create(is_private=True)
            user1 = random.choice(user_pks)
            user2 = random.choice(user_pks)
            while user1 == user2:
                user2 = random.choice(user_pks)

            if not Thread.objects.filter(
                Q(user1_id=user1, user2_id=user2) | Q(user1_id=user2, user2_id=user1)
            ).exists():
                Thread.objects.get_or_create(
                    user1_id=user1,
                    user2_id=user2,
                    room=room,
                )

        self.stdout.write(self.style.SUCCESS("Successfully populated threads"))
