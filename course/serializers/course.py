from rest_framework import serializers

from course.models import Course, Lesson
from course.serializers.lessons import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    """ Course serializer """
    lesson_list = LessonSerializer(many=True, read_only=True, source='lesson')
    lesson_count = serializers.SerializerMethodField()
    course_owner = serializers.SlugRelatedField(slug_field="email", read_only=True)

    @staticmethod
    def get_lesson_count(instance):
        return instance.lesson.count()

    class Meta:
        model = Course
        fields = ('id', 'name', 'lesson_list', 'lesson_count', 'description', 'course_owner',)


class CourseCreateSerializer(serializers.ModelSerializer):
    """ Course create serializer """

    class Meta:
        model = Course
        fields = '__all__'
