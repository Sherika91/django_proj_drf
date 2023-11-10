from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.permissions import IsSelfUser, UserProfileReadOnlySerializer
from users.serializers import UserProfileSerializer, SubscriptionSerializer


class UserProfileListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsSelfUser]


class UserProfileRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):

        if self.request.user == self.get_object():
            return UserProfileSerializer
        return UserProfileReadOnlySerializer


class UserProfileDestroy(generics.DestroyAPIView):
    queryset = User.objects.all()
