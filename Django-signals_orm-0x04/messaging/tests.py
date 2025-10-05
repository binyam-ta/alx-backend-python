# messaging/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


class MessageEditSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="123")
        self.receiver = User.objects.create_user(username="bob", password="123")
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello Bob!"
        )

    def test_message_edit_logs_history(self):
        # Edit the message
        self.message.content = "Hello Bob! How are you?"
        self.message.save()

        # Check if history entry created
        history = MessageHistory.objects.filter(message=self.message)
        self.assertTrue(history.exists())
        self.assertEqual(history.first().old_content, "Hello Bob!")

class UserDeleteSignalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="123")
        self.user2 = User.objects.create_user(username="bob", password="123")
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hi Bob!")
        Notification.objects.create(user=self.user2, message=message)
        MessageHistory.objects.create(message=message, old_content="Old text")

    def test_user_delete_cleans_related_data(self):
        self.user1.delete()
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)
        self.assertEqual(MessageHistory.objects.count(), 0)
        
class ThreadedConversationTest(TestCase):
    def setUp(self):
        self.alice = User.objects.create(username="Alice")
        self.bob = User.objects.create(username="Bob")

        self.root = Message.objects.create(sender=self.alice, receiver=self.bob, content="Hi Bob!")
        self.reply1 = Message.objects.create(sender=self.bob, receiver=self.alice, content="Hey Alice!", parent_message=self.root)
        self.reply2 = Message.objects.create(sender=self.alice, receiver=self.bob, content="How are you?", parent_message=self.reply1)

    def test_recursive_thread(self):
        thread = self.root.get_thread()
        self.assertEqual(len(thread), 2)
        self.assertIn(self.reply1, thread)
        self.assertIn(self.reply2, thread)