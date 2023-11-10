from rest_framework import serializers

from course.serializers.subscription import SubscriptionSerializer
from payment.models import Payment
from users.models import User


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('payment_date', 'amount', 'payment_method')


class UserProfileSerializer(serializers.ModelSerializer):
    payment_history = PaymentHistorySerializer(many=True, read_only=True, source='payments')
    subscription = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups',
                   'user_permissions',)
        read_only_fields = ('id', 'email', 'role', 'payment_history',)
