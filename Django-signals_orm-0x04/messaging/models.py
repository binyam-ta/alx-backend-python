# messaging/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UnreadMessagesManager(models.Manager):
    """Custom manager to filter unread messages for a specific user."""

    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')
        
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='edited_messages')
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()  # custom manager
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
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of message {self.message.id} edited at {self.edited_at}"
