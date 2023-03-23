from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import (ModelSerializer, SerializerMethodField)
from .models import Message, Chat


class ChatSerializer(ModelSerializer):
    user = SerializerMethodField()
    last_message_datetime = SerializerMethodField()
    last_message_text = SerializerMethodField()

    chat_with = PrimaryKeyRelatedField(source='user2', write_only=True, queryset=User.objects.all())

    def validate(self, data):
        user = self.context['request'].user
        chat_with = data['user2']
        if Chat.objects.filter(
                Q(user1=user) & Q(user2=chat_with) | Q(user1=chat_with) & Q(user2=user)
        ).exists():
            raise ValidationError({'chat_with': 'Chat with this user already exists'})
        return data

    def get_user(self, chat):
        request_user = self.context['request'].user
        if chat.user1 == request_user:
            return chat.user2.id
        elif chat.user2 == request_user:
            return chat.user1.id
        else:
            return None

    @staticmethod
    def get_last_message_text(chat):
        try:
            last_message = Message.objects.filter(chat=chat).latest('datetime')
            return last_message.text
        except Message.DoesNotExist:
            return None

    @staticmethod
    def get_last_message_datetime(chat):
        try:
            last_message = Message.objects.filter(chat=chat).latest('datetime')
            return last_message.datetime
        except Message.DoesNotExist:
            return None

    class Meta:
        model = Chat
        fields = ['id', 'user', 'last_message_datetime', 'last_message_text', 'chat_with']


class CurrentUserFilteredPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return Chat.objects.filter(
            Q(user1=user) | Q(user2=user)
        )


class MessageSerializer(ModelSerializer):

    sender = PrimaryKeyRelatedField(read_only=True)
    chat = CurrentUserFilteredPrimaryKeyRelatedField()

    def validate(self, data):
        user = self.context['request'].user
        chat = Chat.objects.get(id=data['chat'].id)
        if user not in (chat.user1, chat.user2):
            raise ValidationError('You cannot send messages in this chat')
        return data

    class Meta:
        model = Message
        fields = ['id', 'sender', 'chat', 'datetime', 'text']
