from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField, Serializer

from .models import Post, Comment


class PostSerializer(ModelSerializer):

    comments = SerializerMethodField()

    @staticmethod
    def get_comments(post):
        return [
            {'user': comment.user.id, 'text': comment.text}
            for comment in Comment.objects.filter(post=post)
        ]

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['likes', 'comments', 'author']
        exlude = ['author']


class CommentSerializer(ModelSerializer):
    text = CharField(style={'base_template': 'textarea.html'})

    class Meta:
        model = Comment
        fields = ['text']


class LikeSerializer(Serializer):
    message = CharField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
