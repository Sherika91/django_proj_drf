from django.urls import reverse
from rest_framework import status

from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken
from course.models import Course, Lesson
from subscription.models import Subscription
from users.models import User


class BaseTestCase(APITestCase):
    email = 'test@gmail.com'
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

        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            course_owner=self.user,
        )

        self.lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Test Description',
            lesson_owner=self.user,
            course=self.course,
        )

        self.subscription = Subscription.objects.create(
            course=self.course,
            user=self.user,
            is_subscribed=True,
        )

        self.client = APIClient()
        # Get Access Token For Current User (Moderator)
        access_token = AccessToken.for_user(self.user)
        self.client.force_authenticate(user=self.user, token=access_token)

    def tearDown(self):
        self.course.delete()
        self.user.delete()
        self.subscription.delete()


class CourseTestCases(BaseTestCase):
    def test_course_create(self):
        """ Test For Creating Course Object """
        response = self.client.post(reverse("course:course-list"), data={
            'name': 'Test Course 2',
            'description': 'Test Description 2',
            'course_owner': self.user.pk
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(),
                         {
                             'id': 2,
                             'lesson_list': [],
                             'lesson_count': 0,
                             'name': 'Test Course 2',
                             'preview': None,
                             'description': 'Test Description 2',
                             'course_owner': self.user.pk
                         }
                         )

    def test_get_course_list(self):
        """ Test To Get Course Objects List """
        response = self.client.get(reverse("course:course-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK, )
        self.assertEqual(response.json(),
                         {
                             'count': 1,
                             'next': None,
                             'previous': None,
                             'results': [
                                 {
                                     'id': self.course.pk,
                                     'lesson_list': [{
                                         'id': self.lesson.pk,
                                         'name': 'Test Lesson',
                                         'description': 'Test Description',
                                         'preview': None,
                                         'video': None,
                                         'course': self.course.pk,
                                         'lesson_owner': self.user.pk
                                     }],
                                     'lesson_count': 1,
                                     'name': 'Test Course',
                                     'preview': None,
                                     'description': 'Test Description',
                                     'course_owner': self.user.pk}]})

    def test_get_course(self):
        """ Test For Getting Course Object """
        response = self.client.get(reverse("course:course-detail", args=[self.course.pk]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': self.course.pk,
                             'lesson_list': [{
                                 'course': self.course.pk,
                                 'description': 'Test Description',
                                 'id': self.lesson.pk,
                                 'lesson_owner': self.user.pk,
                                 'name': 'Test Lesson',
                                 'preview': None,
                                 'video': None}],
                             'lesson_count': 1,
                             'name': 'Test Course',
                             'preview': None,
                             'description': 'Test Description',
                             'course_owner': self.user.pk
                         }
                         )

    def test_update_course(self):
        """ Test For Updating Course Object """
        response = self.client.patch(reverse("course:course-detail", args=[self.course.pk]),
                                     data={
                                         'name': 'Test Course Update',
                                         'description': 'Test Description Update',
                                     })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': self.course.pk,
                             'lesson_list': [{
                                 'course': self.course.pk,
                                 'description': 'Test Description',
                                 'id': self.lesson.pk,
                                 'lesson_owner': self.user.pk,
                                 'name': 'Test Lesson',
                                 'preview': None,
                                 'video': None}],
                             'lesson_count': 1,
                             'name': 'Test Course Update',
                             'preview': None,
                             'description': 'Test Description Update',
                             'course_owner': self.user.pk
                         })

    def test_delete_course(self):
        """ Test For Deleting Course Object """
        response = self.client.delete(reverse("course:course-detail", args=[self.course.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LessonTestCases(BaseTestCase):
    def test_lesson_create(self):
        response = self.client.post(reverse("course:lesson-create"), data={
            'name': 'Test Lesson',
            'description': 'Test Description',
            'lesson_owner': self.user.id,
            'course': self.course.id,
        }
                                    )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(),
                         {
                             'id': 3,
                             'name': 'Test Lesson',
                             'description': 'Test Description',
                             'preview': None,
                             'video': None,
                             'course': self.course.pk,
                             'lesson_owner': self.user.pk,
                         }
                         )

    def test_lesson_get_list(self):
        response = self.client.get(reverse("course:lesson-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {'id': self.lesson.pk,
                 'course': 'Test Course',
                 'name': 'Test Lesson',
                 'description': 'Test Description',
                 'preview': None,
                 'video': None,
                 'lesson_owner': self.user.pk,

                 }
            ]
        }
                         )

    def test_get_lesson(self):
        response = self.client.get(reverse("course:lesson-detail", args=[self.lesson.pk]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': self.lesson.pk,
                             'name': 'Test Lesson',
                             'description': 'Test Description',
                             'preview': None,
                             'video': None,
                             'course': self.course.pk,
                             'lesson_owner': self.user.pk,
                         }
                         )

    def test_lesson_update(self):
        response = self.client.patch(reverse("course:lesson-update", args=[self.lesson.pk]), data={
            'name': 'Test Lesson Update',
            'description': 'Test Description Update',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': self.lesson.pk,
                             'name': 'Test Lesson Update',
                             'description': 'Test Description Update',
                             'preview': None,
                             'video': None,
                             'course': self.course.pk,
                             'lesson_owner': self.user.pk,
                         }
                         )

    def test_lesson_delete(self):
        response = self.client.delete(reverse("course:lesson-delete", args=[self.lesson.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTestCases(BaseTestCase):
    def test_subscription_create(self):
        response = self.client.post(reverse("subscription:create"), data={
            'course': self.course.pk,
            'user': self.user.pk,
            'is_subscribed': False,
        }
                                    )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(),
                         {
                             'id': 2,
                             'course': self.course.pk,
                             'user': self.user.pk,
                             'is_subscribed': False,
                         }
                         )

    def test_subscription_get_list(self):
        response = self.client.get(reverse("subscription:list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         [{
                             'id': self.subscription.pk,
                             'is_subscribed': True,
                             'user': self.user.pk,
                             'course': self.course.pk}
                         ])

    def test_unsubscribe(self):
        response = self.client.delete(reverse("subscription:delete", args=[self.subscription.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
