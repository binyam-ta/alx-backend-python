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


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # add OrderingFilter
    filterset_class = MessageFilter
    ordering_fields = ['timestamp']  # allow ordering by timestamp
    ordering = ['-timestamp']        # default ordering (newest first)

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
