##/from rest_framework import serializers
'''
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['sent_at', 'sender']

    def create(self, validated_data):
        # Automatically set sender to request.user
        user = self.context['request'].user
        validated_data['sender'] = user
        return super().create(validated_data)

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)  # Nested messages

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        # Create conversation and add participants from request data
        participants_data = self.context['request'].data.get('participants', [])
        conversation = Conversation.objects.create()
        if participants_data:
            conversation.participants.set(participants_data)
        return conversation
'''

from rest_framework import serializers
from .models import User, Conversation, Message

# ---------------------------
# User Serializer
# ---------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'role']

# ---------------------------
# Message Serializer
# ---------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # nested user info

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']

    # ---------------------------
    # Validate that sender is in the conversation
    # ---------------------------
    def validate(self, data):
        sender = self.context['request'].user
        conversation = data.get('conversation')

        if sender not in conversation.participants.all():
            raise serializers.ValidationError("You can only send messages to conversations you are a participant of.")
        
        return data

# ---------------------------
# Conversation Serializer
# ---------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()  # custom field to include messages

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    # ---------------------------
    # Method to get messages
    # ---------------------------
    def get_messages(self, obj):
        messages = obj.message_set.all().order_by('sent_at')
        return MessageSerializer(messages, many=True).data

    # ---------------------------
    # Example validation
    # ---------------------------
    def validate(self, data):
        if not data.get('participants'):
            raise serializers.ValidationError("A conversation must have at least one participant.")
        return data
