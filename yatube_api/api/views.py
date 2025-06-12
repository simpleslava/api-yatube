"""API-представления для работы с моделями Post, Group и Comment."""

from posts.models import Comment, Group, Post
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

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
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """Получение комментариев для конкретного поста."""
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        """Создание комментария с привязкой к посту и пользователю."""
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Обновление комментария."""
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=False
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
