from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Message, MessageHistory
from django.contrib.auth.decorators import login_required

# Threaded messages view
@login_required
def get_threaded_messages(request, conversation_id):
    messages = Message.objects.filter(receiver=request.user, parent_message__isnull=True)\
        .select_related('sender')\
        .prefetch_related('replies')

    def build_thread(message):
        return {
            "id": message.id,
            "sender": message.sender.username,
            "content": message.content,
            "timestamp": message.timestamp,
            "edited": message.edited,
            "replies": [build_thread(reply) for reply in message.replies.all()]
        }

    data = [build_thread(msg) for msg in messages]
    return JsonResponse(data, safe=False)

# Inbox showing only unread messages
@login_required
def inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user)
    data = [{"id": msg.id, "sender": msg.sender.username, "content": msg.content, "timestamp": msg.timestamp} for msg in unread_messages]
    return JsonResponse(data, safe=False)

# Message edit history
@login_required
def message_history(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    history = message.history.all().values('old_content', 'edited_at')
    return JsonResponse(list(history), safe=False)
