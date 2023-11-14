from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    Message = "Yor are not Owner!"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.course_owner:
            return True
        return False
