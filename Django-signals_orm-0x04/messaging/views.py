from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message, MessageHistory

# Inbox showing only unread messages, optimized
@login_required
@cache_page(60)  # Cache results for 60 seconds
def inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user)\
        .select_related('sender')\
        .only('id', 'sender__username', 'content', 'timestamp')
    
    data = [
        {
            "id": msg.id,
            "sender": msg.sender.username,
            "content": msg.content,
            "timestamp": msg.timestamp
        } 
        for msg in unread_messages
    ]
    return JsonResponse(data, safe=False)

# Threaded messages view with prefetch and select
@login_required
@cache_page(60)  # Cache threaded conversation for 60 seconds
def get_threaded_messages(request, conversation_id):
    messages = Message.objects.filter(receiver=request.user, parent_message__isnull=True)\
        .select_related('sender')\
        .prefetch_related('replies')\
        .only('id', 'sender__username', 'content', 'timestamp', 'edited')
    
    def build_thread(message):
        return {
            "id": message.id,
            "sender": message.sender.username,
            "content": message.content,
            "timestamp": message.timestamp,
            "edited": message.edited,
            "replies": [build_thread(reply) for reply in message.replies.all().select_related('sender').only('id', 'sender__username', 'content', 'timestamp', 'edited')]
        }

    data = [build_thread(msg) for msg in messages]
    return JsonResponse(data, safe=False)

# Message edit history
@login_required
@cache_page(60)
def message_history(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    history = message.history.all().only('old_content', 'edited_at')
    data = [{"old_content": h.old_content, "edited_at": h.edited_at} for h in history]
    return JsonResponse(data, safe=False)
