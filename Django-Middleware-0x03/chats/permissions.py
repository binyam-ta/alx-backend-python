from rest_framework import permissions
from .models import Conversation, Message
from rest_framework.status import HTTP_403_FORBIDDEN

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants of a conversation to access messages/conversations.
    Supports all HTTP methods: GET, POST, PUT, PATCH, DELETE.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # If object is a Conversation
        if isinstance(obj, Conversation):
            return user in obj.participants.all()

        # If object is a Message, check the conversation’s participants
        if isinstance(obj, Message):
            return user in obj.conversation.participants.all()

        return False
