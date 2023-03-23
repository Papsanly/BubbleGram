from django.contrib.auth.models import User
from django.db.models import Model, CASCADE, ForeignKey, DateTimeField, TextField


class Chat(Model):
    user1 = ForeignKey(User, on_delete=CASCADE, null=False, related_name='chats_as_user1')
    user2 = ForeignKey(User, on_delete=CASCADE, null=False, related_name='chats_as_user2')

    def __str__(self):
        return f'{self.user1} talks with {self.user2}'


class Message(Model):
    chat = ForeignKey(Chat, on_delete=CASCADE, null=False)
    sender = ForeignKey(User, on_delete=CASCADE, null=False)
    datetime = DateTimeField(auto_now_add=True)
    text = TextField(null=False)

    def __str__(self):
        return f'{self.sender}: {self.text}'
