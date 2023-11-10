from django.urls import path

from .apps import PaymentConfig
from . import views

app_name = PaymentConfig.name


urlpatterns = [
    # PAYMENT URLS USING "GENERICS APIVIEW"
    path('payment/', views.PaymentListAPIView.as_view(), name='payment-list'),
    path('payment/create/', views.PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payment/<int:pk>/detail/', views.PaymentRetrieveAPIView.as_view(), name='payment-detail'),

]
