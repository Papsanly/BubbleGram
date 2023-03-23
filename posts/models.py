from django.contrib.auth.models import User
from django.db.models import Model, ImageField, TextField, ManyToManyField, ForeignKey, CASCADE, SET_NULL


class Post(Model):
    author = ForeignKey(User, on_delete=CASCADE, null=False, related_name='posts')
    photo = ImageField(null=False)
    description = TextField()
    likes = ManyToManyField(User, related_name='likes')
    comments = ManyToManyField(User, through='Comment', related_name='comments')

    def __str__(self):
        return f'Post by {self.author.username} ({self.id})'


class Comment(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    post = ForeignKey(Post, on_delete=CASCADE)
    text = TextField(null=False, blank=True)

    def __str__(self):
        return f'Comment by {self.user.username}: {self.text}'
