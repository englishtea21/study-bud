from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from base.models import Topic, Room, User
from django.db import models


@receiver(post_delete, sender=Room)
def handle_room_deletion(sender, instance, **kwargs):
    topics_without_rooms = Topic.objects.filter(rooms__isnull=True)

    for topic in topics_without_rooms:
        topic.delete()
