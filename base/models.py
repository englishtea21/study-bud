from django.db import models
from django.contrib.auth.models import AbstractUser
from . import managers


class User(AbstractUser):
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    bio = models.TextField(null=True, blank=True, max_length=500)

    profile_picture = models.ImageField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name"]
    
    class Meta:
        permissions = [
            ("vote_room", "Upvotes/Downvotes functionality on a room"),
        ]

    def __str__(self):
        return str(self.username)


class Topic(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic, related_name="rooms", blank=False)
    name = models.CharField(max_length=200)
    # blank=True <=> разрешается оставить пустое поле при заполнении формы
    # null=True <=> разрешается хранить объект с пустым значением поля
    description = models.TextField(null=True, blank=True, max_length=500)
    participants = models.ManyToManyField(User, related_name="rooms", blank=True)
    upvotes = models.ManyToManyField(
        User,
        related_name="upvotes",
        blank=True,
    )
    downvotes = models.ManyToManyField(
        User,
        related_name="downvotes",
        blank=True,
    )
    # auto_now=True <=> сохраняет время обновления
    updated = models.DateTimeField(auto_now=True)
    # auto_now_add=True <=> сохраняет момент создания
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # задает сортировку объектов в коллекции по двум параметрам
        ordering = ["-updated", "-created"]

    def getvotes(self):
        return self.upvotes.count() - self.downvotes.count()

    def __str__(self):
        return self.name


class Message(models.Model):
    max_str_length = 50
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # когда комната удаляется, удаляются все сообщения внутри нее
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    # auto_now=True <=> сохраняет время обновления
    updated = models.DateTimeField(auto_now=True)
    # auto_now_add=True <=> сохраняет момент создания
    created = models.DateTimeField(auto_now_add=True)
    replyto = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        # задает сортировку объектов в коллекции по двум параметрам
        ordering = ["-created"]

    def __str__(self):
        return self.body[: self.max_str_length]
