from django.db.models import Q
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Message, Chat
from .serializers import MessageSerializer, ChatSerializer


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('chat', openapi.IN_QUERY, description="Filter by chat", type=openapi.TYPE_INTEGER),
        ]
    )
)
class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        user = self.request.user
        chat = self.request.query_params.get('chat')
        messages = Message.objects.filter(
            Q(chat__user1=user) | Q(chat__user2=user)
        )
        if chat:
            messages = messages.filter(chat=chat)
        return messages


class ChatViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user1=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(
            Q(user1=user) | Q(user2=user)
        )
