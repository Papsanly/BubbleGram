from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, LikeSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], serializer_class=LikeSerializer)
    def like(self, request, pk=None):
        user = self.request.user
        post = Post.objects.get(pk=pk)
        post.likes.add(user)
        serializer = LikeSerializer({'message': 'Liked successfully'})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], serializer_class=CommentSerializer)
    def comment(self, request, pk=None):
        user = self.request.user
        text = self.request.data['text']
        post = Post.objects.get(pk=pk)
        comment = Comment.objects.create(user=user, post=post, text=text)
        comment.save()
        serializer = self.get_serializer({'text': text})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
