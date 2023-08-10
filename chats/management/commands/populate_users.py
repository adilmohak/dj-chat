import json
import string
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Populates users from a JSON file"

    def generate_random_password(self):
        length = 12  # You can adjust the length of the password
        characters = string.ascii_letters + string.digits + string.punctuation
        return "".join(random.choice(characters) for _ in range(length))

    def handle(self, *args, **options):
        with open("data/sample_users.json", "r") as json_file:
            user_data = json.load(json_file)

            User = get_user_model()
            created_users = []

            for data in user_data:
                username = data["username"]
                email = data["email"]
                first_name = data["first_name"]
                last_name = data["last_name"]
                password = self.generate_random_password()

                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                        "password": make_password(password),
                    },
                )

                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Created user: {user.username}")
                    )
                    created_users.append(user.username)
                else:
                    self.stdout.write(
                        self.style.WARNING(f"User already exists: {user.username}")
                    )

            self.stdout.write(
                self.style.SUCCESS(f"Successfully populated {len(created_users)} users")
            )
