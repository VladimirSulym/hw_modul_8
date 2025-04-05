from rest_framework import serializers

from lms.models import Course, Lesson, Payment
from lms.validators import DataInputValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            DataInputValidator(fields="description"),
            DataInputValidator(fields="title"),
        ]


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"
        validators = [
            DataInputValidator(fields="title"),
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    course_count_lessons = serializers.SerializerMethodField()
    info_lessons = LessonSerializer(read_only=True, many=True, source="lessons")

    @staticmethod
    def get_course_count_lessons(obj):
        return Course.objects.get(id=obj.id).lessons.count()

    class Meta:
        model = Course
        fields = ["title", "city", "course_count_lessons", "info_lessons"]


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"
