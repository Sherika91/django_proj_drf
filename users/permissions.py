from rest_framework import permissions, serializers

from .models import User


class IsSelfUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        return False


class UserProfileReadOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("password", "last_name")
