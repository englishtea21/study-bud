from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from base.models import Topic, Room, User
from django.contrib.auth.models import Permission
from django.db import models


@receiver(post_delete, sender=Room)
def handle_room_deletion(sender, instance, **kwargs):
    topics_without_rooms = Topic.objects.filter(rooms__isnull=True)

    for topic in topics_without_rooms:
        topic.delete()


@receiver(post_save, sender=User)
def assign_default_permission(sender, instance, created, **kwargs):
    if created:
        # Назначаем разрешение пользователю только при его создании
        permission_list = [
            "add_topic",
            "vote_room",
            "add_message",
            "delete_message",
            "add_room",
            "delete_room",
        ]
        for permission_name in permission_list:
            permission = Permission.objects.get(codename=permission_name)
            instance.user_permissions.add(permission)
