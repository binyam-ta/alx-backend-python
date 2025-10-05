from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from .models import Message
from .managers import UnreadMessagesManager


# Custom function to recursively build message threads
def build_thread(message):
    return {
        "id": message.id,
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "timestamp": message.timestamp,
        "edited": message.edited,
        "edited_by": getattr(message, "edited_by", None),
        "replies": [
            build_thread(reply) for reply in message.replies.all()
            .select_related('sender')
            .only('id', 'sender__username', 'content', 'timestamp', 'edited', 'edited_by')
        ]
    }


@method_decorator([login_required, cache_page(60)], name='dispatch')
class SentMessagesView(View):
    """
    Returns all messages sent by the logged-in user in threaded format
    """
    def get(self, request):
        # Filter messages sent by the user
        messages = Message.objects.filter(sender=request.user, parent_message__isnull=True) \
            .select_related('sender', 'receiver') \
            .prefetch_related('replies') \
            .only('id', 'sender__username', 'receiver__username', 'content', 'timestamp', 'edited', 'edited_by')

        # Build threaded messages recursively
        data = [build_thread(msg) for msg in messages]
        return JsonResponse({"sent_messages": data}, safe=False)


@method_decorator([login_required, cache_page(60)], name='dispatch')
class UnreadMessagesView(View):
    """
    Returns all unread messages for the logged-in user
    """
    def get(self, request):
        # Use the custom manager to get unread messages
        unread_messages = Message.unread.unread_for_user(request.user) \
            .select_related('sender', 'receiver') \
            .only('id', 'sender__username', 'receiver__username', 'content', 'timestamp', 'edited', 'edited_by')

        data = [
            {
                "id": msg.id,
                "sender": msg.sender.username,
                "receiver": msg.receiver.username,
                "content": msg.content,
                "timestamp": msg.timestamp,
                "edited": msg.edited,
                "edited_by": getattr(msg, "edited_by", None)
            }
            for msg in unread_messages
        ]
        return JsonResponse({"unread_messages": data}, safe=False)
