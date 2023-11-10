from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from course.serializers.subscription import SubscriptionSerializer


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        subscription = serializer.save()
        subscription.user = self.request.user
        subscription.course = self.request.pk
        subscription.save()
