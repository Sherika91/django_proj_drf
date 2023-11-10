from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .models import Payment
from .serializers import PaymentSerializer


# PAYMENT CRUD VIEWS USING GENERICS APIVIEW
class PaymentListAPIView(generics.ListAPIView):
    """ Payment List view """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['payment_date', 'payment_method', 'course_payment', 'lesson_payment']
    ordering_fields = ('payment_date',)


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Payment Create View """
    serializer_class = PaymentSerializer


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """ Payment Details(Retrieve) View  """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
