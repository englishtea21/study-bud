# Generated by Django 4.2.3 on 2023-08-15 08:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_message_options_alter_topic_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='downvotes',
            field=models.ManyToManyField(blank=True, null=True, related_name='downvotes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='room',
            name='upvotes',
            field=models.ManyToManyField(blank=True, null=True, related_name='upvotes', to=settings.AUTH_USER_MODEL),
        ),
    ]
