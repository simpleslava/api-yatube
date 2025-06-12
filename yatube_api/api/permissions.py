"""Модуль с настройками прав доступа для API."""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только владельцам объекта для небезопасных методов.

    Для безопасных методов (GET, HEAD, OPTIONS) требуется только аутентификация.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return obj.author == request.user
