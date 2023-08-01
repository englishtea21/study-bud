from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from base.models import Topic, Room, User
from django.db import models


@receiver(post_delete, sender=Room)
def handle_room_deletion(sender, instance, **kwargs):
    topics_without_rooms = Topic.objects.filter(rooms__isnull=True)

    for topic in topics_without_rooms:
        topic.delete()


# @receiver(post_delete, sender=User)
# def handle_profile_picture_deletion(sender, instance, **kwargs):
#     instance.profile_picture = models.ImageField(null=False, blank=True, default='avatar.svg')

# @receiver(post_save, sender=User)
# def handle_field_change(sender, instance, **kwargs):
#     # if not created:  # Выполнять действия только при обновлении объекта
#     #     previous_field_value = User.objects.get(pk=instance.pk).profile_picture
#     # print('** Hello! I am image signal **')
#     # checking if image is empty
#     if not bool(instance.profile_picture):
#         instance.profile_picture = models.ImageField(null=False, blank=True, default='avatar.svg')
#         # Действия, которые нужно выполнить при изменении поля field_name
#         # Замените field_name на имя конкретного поля в вашей модели
#         print("* Default avatar *")
