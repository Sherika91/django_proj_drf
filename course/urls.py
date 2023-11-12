from django.urls import path

from course.apps import CourseConfig
from rest_framework.routers import DefaultRouter

from course.views import lessons, course, subscription

app_name = CourseConfig.name

router = DefaultRouter()
router.register(r'course', course.CourseViewSet, basename='course')

urlpatterns = [
    # LESSON URLS
    path('lesson/', lessons.LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/create/', lessons.LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/<int:pk>/detail/', lessons.LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('lesson/<int:pk>/update/', lessons.LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/<int:pk>/delete/', lessons.LessonDestroyAPIView.as_view(), name='lesson-delete'),
    # SUBSCRIPTION URLS
    path('course/subscribe/', subscription.SubscriptionCreateAPIView.as_view(), name='course-subscribe'),
    path('course/unsubscribe/', subscription.SubscriptionDestroyAPIView.as_view(), name='course-unsubscribe'),

] + router.urls
