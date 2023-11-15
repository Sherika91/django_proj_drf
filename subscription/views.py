from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from subscription.models import Subscription
from subscription.serializers import SubscriptionSerializer


class SubscriptionCreateView(generics.CreateAPIView):
    """ API endpoint that allows a user to subscribe to a plan. """
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionListView(generics.ListAPIView):
    """ API endpoint that allows a user to view their subscriptions. """
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user, is_subscribed=True)


class SubscriptionDestroyView(generics.DestroyAPIView):
    """ API endpoint that allows a user to delete a subscription. """
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)