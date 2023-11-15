from django.urls import path

from .apps import SubscriptionConfig
from .views import SubscriptionCreateView, SubscriptionListView, SubscriptionDestroyView

app_name = SubscriptionConfig.name

urlpatterns = [
    path('subscribe/', SubscriptionCreateView.as_view(), name='create'),
    path('subscriptions/', SubscriptionListView.as_view(), name='list'),
    path('unsubscribe/<int:pk>/', SubscriptionDestroyView.as_view(), name='delete'),

]
