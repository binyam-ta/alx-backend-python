# from rest_framework import viewsets, status, filters
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import User, Conversation, Message
# from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

# # ---------------------------
# # Conversation ViewSet
# # ---------------------------
# class ConversationViewSet(viewsets.ModelViewSet):
#     queryset = Conversation.objects.all()
#     serializer_class = ConversationSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.OrderingFilter]
#     ordering_fields = ['created_at']
#     ordering = ['-created_at']

#     def perform_create(self, serializer):
#         # Add the requesting user as a participant
#         serializer.save(participants=[self.request.user])

# # ---------------------------
# # Message ViewSet
# # ---------------------------
# class MessageViewSet(viewsets.ModelViewSet):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.OrderingFilter]
#     ordering_fields = ['sent_at']
#     ordering = ['sent_at']

#     def perform_create(self, serializer):
#         # Set the sender to the requesting user
#         serializer.save(sender=self.request.user)


from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_action_with_access_check(self, request, message):
        """
        Checks if the request.user is participant in the conversation.
        Returns HTTP_403_FORBIDDEN if not.
        """
        conversation_id = message.conversation.id  # <- now explicitly used
        if request.user not in message.conversation.participants.all():
            return Response(
                {"detail": f"Not a participant of conversation {conversation_id}"},
                status=status.HTTP_403_FORBIDDEN
            )
        return None

    def update(self, request, *args, **kwargs):
        message = self.get_object()
        forbidden = self.perform_action_with_access_check(request, message)
        if forbidden:
            return forbidden
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        message = self.get_object()
        forbidden = self.perform_action_with_access_check(request, message)
        if forbidden:
            return forbidden
        return super().destroy(request, *args, **kwargs)
