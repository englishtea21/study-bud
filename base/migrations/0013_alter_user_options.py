# Generated by Django 4.2.3 on 2023-08-22 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_rename_reply_to_message_replyto'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('vote_room', 'Upvotes/Downvotes functionality on a room')]},
        ),
    ]
