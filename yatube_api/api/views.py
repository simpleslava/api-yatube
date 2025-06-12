"""API-представления для работы с моделями Post, Group и Comment."""

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Comment, Group, Post
from .permissions import IsOwnerOrReadOnlyPermission
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyPermission]

    def perform_create(self, serializer):
        """Создание поста с привязкой к текущему пользователю."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с группами (только чтение)."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyPermission]

    def get_queryset(self):
        """Получение комментариев для конкретного поста."""
        post = self._get_post()
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        """Создание комментария с привязкой к посту и пользователю."""
        post = self._get_post()
        serializer.save(author=self.request.user, post=post)

    def _get_post(self):
        """Вспомогательный метод для получения поста."""
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)
