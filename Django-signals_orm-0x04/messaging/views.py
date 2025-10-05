# messaging/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from .models import Message

@login_required
def delete_user(request):
    """Allow a user to delete their own account."""
    user = request.user
    username = user.username
    user.delete()
    messages.success(request, f"User '{username}' and all related data have been deleted.")
    return redirect("home")  # Replace 'home' with your home page URL name

def conversation_detail(request, message_id):
    """Fetch a conversation and all its replies efficiently."""
    root_message = get_object_or_404(
        Message.objects.select_related("sender", "receiver").prefetch_related("replies__sender", "replies__receiver"),
        id=message_id
    )

    thread = root_message.get_thread()

    return render(request, "messaging/conversation_detail.html", {
        "root_message": root_message,
        "thread": thread
    })
   
def unread_messages_view(request):
    user = request.user
    unread_messages = Message.unread.for_user(user)

    return render(request, "messaging/unread_messages.html", {
        "unread_messages": unread_messages
    })    