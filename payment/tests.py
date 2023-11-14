from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, force_authenticate
from rest_framework_simplejwt.tokens import AccessToken

from course.models import Course
from payment.models import Payment
from users.models import User


class BaseTestCase(APITestCase):
    email = 'user@gmail.com'
    password = 'test1234'

    def setUp(self):
        self.user = User.objects.create(
            email=self.email,
            first_name='Admin',
            last_name='Admin',
            phone='12345678',
            role='member',  # Can Be Member or Moderator
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        self.user.set_password(self.password)
        self.user.save()

        self.client = APIClient()
        # Get Access Token For Current User (Member)
        access_token = AccessToken.for_user(self.user)
        self.client.force_authenticate(user=self.user, token=access_token)

        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            course_owner=self.user,
        )

        self.payment = Payment.objects.create(
            user=self.user,
            amount=1000,
            payment_method='Card',
            payment_owner=self.user,
            course_payment=self.course,
        )

    def tearDown(self):
        self.user.delete()
        self.payment.delete()
        self.course.delete()


class PaymentTestCases(BaseTestCase):

    def test_get_user_payment_list(self):
        response = self.client.get(reverse("payment:payment-list"))
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': self.payment.pk,
                             'user': 'user@gmail.com',
                             'user_name': 'Admin',
                             'user_last_name': 'Admin',
                             'course_payment': self.course.pk,
                             'lesson_payment': None,
                             'payment_date': '2023-11-14T12:21:15.315465Z',
                             'amount': '1000.00',
                             'payment_method': 'Card',
                             'payment_owner': self.user.pk}
                         )

        def test_get_user_payment_detail(self):
            response = self.client.get(reverse("payment:payment-detail", args=[self.user.pk]))

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(),
                             {
                                 'id': self.payment.pk,
                                 'user': 'user@gmail.com',
                                 'user_name': 'Admin',
                                 'user_last_name': 'Admin',
                                 'course_payment': None,
                                 'lesson_payment': None,
                                 'payment_date': self.payment.payment_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                 'amount': '1000.00',
                                 'payment_method': 'Card',
                                 'payment_owner': self.user.pk})
