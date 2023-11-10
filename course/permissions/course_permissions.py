from rest_framework import permissions

from users.models import UserRoles


class IsOwner(permissions.BasePermission):
    Message = "Yor are not Owner!"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.course_owner:
            return True
        return False


class IsModerator(permissions.BasePermission):
    Message = "Yor are not Moderator!"

    def has_permission(self, request, view):
        if request.user.role == UserRoles.MODERATOR:
            return True
        return False


class IsNotModerator(permissions.BasePermission):
    Message = "Yor are not Moderator!"

    def has_permission(self, request, view):
        if request.user.role != UserRoles.MODERATOR:
            return True
        return False
