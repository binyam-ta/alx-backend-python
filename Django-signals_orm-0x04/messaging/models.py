# messaging/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UnreadMessagesManager(models.Manager):
    """Custom manager to filter unread messages for a specific user."""

    def for_user(self, user):
        """
        Returns unread messages for the given user.
        Uses `.only()` to optimize by fetching minimal fields.
        """
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "content", "timestamp")
            .select_related("sender")  # fetch sender in the same query
        )
        
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    edited = models.BooleanField(default=False)

    # 👇 Self-referential relationship for threaded replies
    parent_message = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )
       # 👇 New field for message read status
    read = models.BooleanField(default=False)

    # 👇 Default and custom managers
    objects = models.Manager()            # The default manager
    unread = UnreadMessagesManager()      # Our custom unread messages manager

    def mark_as_read(self):
        """Mark a message as read."""
        if not self.read:
            self.read = True
            self.save(update_fields=["read"])
            
    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:30]}"

    def get_thread(self):
        """
        Recursively fetch all replies to this message.
        """
        replies = self.replies.all().select_related("sender", "receiver").prefetch_related("replies")
        thread = []
        for reply in replies:
            thread.append(reply)
            thread.extend(reply.get_thread())  # recursive call
        return thread


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message.content[:30]}"


class MessageHistory(models.Model):
    """Stores old versions of messages before edits."""
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of message {self.message.id} edited at {self.edited_at}"
