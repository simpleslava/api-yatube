"""Модуль с настройками прав доступа для API."""

from rest_framework import permissions


class IsOwnerOrReadOnlyPermission(permissions.BasePermission):
    """
    Разрешает доступ только владельцам объекта для небезопасных методов.

    Для безопасных методов (GET, HEAD, OPTIONS) нужна только аутентификация.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
