# Generated by Django 4.1.1 on 2023-07-30 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chats", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="discussionroom",
            name="mode",
        ),
        migrations.RemoveField(
            model_name="room",
            name="is_support",
        ),
        migrations.DeleteModel(
            name="PageSupport",
        ),
    ]
