from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Message, Conversation

# Example: caching messages list for a conversation
@method_decorator(cache_page(60), name='dispatch')  # cache for 60 seconds
def messages_list(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation).select_related('sender')
    data = [
        {
            "id": msg.id,
            "sender": msg.sender.username,
            "content": msg.content,
            "timestamp": msg.timestamp,
        }
        for msg in messages
    ]
    return JsonResponse(data, safe=False)
