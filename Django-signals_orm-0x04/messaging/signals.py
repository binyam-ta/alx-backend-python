# messaging/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Signal to create a notification when a new message is sent."""
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


# Log message edits
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        old = Message.objects.get(pk=instance.pk)
        if old.content != instance.content:
            MessageHistory.objects.create(message=instance, old_content=old.content)
            instance.edited = True
  # mark as edited

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """Automatically delete related data when a user is deleted."""
    # Delete messages sent or received by this user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications related to this user
    Notification.objects.filter(user=instance).delete()

    # Delete all message histories linked to messages from this user
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()