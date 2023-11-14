from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from course.permissions.subscription_permissions import IsOwner
from course.serializers.subscription import SubscriptionSerializer


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.request.user
