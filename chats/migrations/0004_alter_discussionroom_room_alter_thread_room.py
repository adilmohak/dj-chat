# Generated by Django 4.1.1 on 2023-08-11 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("chats", "0003_alter_discussionroom_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discussionroom",
            name="room",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="discussion_room",
                to="chats.room",
            ),
        ),
        migrations.AlterField(
            model_name="thread",
            name="room",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="room_thread",
                to="chats.room",
            ),
        ),
    ]
