from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Allow only authenticated users
    - Allow only conversation participants to access messages
    """
    def has_object_permission(self, request, view, obj):
        # Ensure the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # If object is a Conversation, check participants
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # If object is a Message, check the conversation’s participants
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
