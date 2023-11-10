from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from payment.models import Payment, Course, Lesson
from users.models import User


class PaymentSerializer(serializers.ModelSerializer):
    """ Payment serializer """
    user = SlugRelatedField(slug_field="email", queryset=User.objects.all())
    user_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)

    course_payment = serializers.SerializerMethodField(read_only=True)
    lesson_payment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"

    @staticmethod
    def get_course_payment(instance):
        course_value = instance.course_payment

        if course_value:
            # Try to retrieve the object by its primary key
            try:
                course = Course.objects.get(pk=course_value)
                return str(course.id)
            except Course.DoesNotExist:
                return "Object not found"

    @staticmethod
    def get_lesson_payment(instance):
        lesson_value = instance.lesson_payment

        if lesson_value:
            # Try to retrieve the object by its primary key
            try:
                lesson = Lesson.objects.get(pk=lesson_value)
                return str(lesson.id)
            except Lesson.DoesNotExist:
                return "Object not found"
