from rest_framework.permissions import BasePermission


class IsModerators(BasePermission):
    message = "Только модераторы могут выполнять эту операцию"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()
        # Проверяет, является ли текущий пользователь модератором


class IsOwner(BasePermission):
    message = "Только владелец курса или урока может выполнять эту операцию"

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
