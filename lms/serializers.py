from rest_framework import serializers

from lms.models import Course, Lesson, Payment, Subscription
from lms.validators import DataInputValidator


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            DataInputValidator(fields="description"),
            DataInputValidator(fields="title"),
        ]


class CourseSerializer(serializers.ModelSerializer):
    info_sub = serializers.SerializerMethodField()
    # info_sub = SubscriptionSerializer(read_only=True, many=True, source="subscriptions")

    @staticmethod
    def get_info_sub(obj):
        if Subscription.objects.filter(course=obj).exists():
            return True
        return False

    class Meta:
        model = Course
        fields = ["id", "title", "avatar", "city", "owner", "info_sub"]
        validators = [
            DataInputValidator(fields="title"),
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    course_count_lessons = serializers.SerializerMethodField()
    info_sub = serializers.SerializerMethodField()
    info_lessons = LessonSerializer(read_only=True, many=True, source="lessons")

    @staticmethod
    def get_course_count_lessons(obj):
        return Course.objects.get(id=obj.id).lessons.count()

    @staticmethod
    def get_info_sub(obj):
        if Subscription.objects.filter(course=obj).exists():
            return True
        return False

    class Meta:
        model = Course
        fields = ["title", "city", "course_count_lessons", "info_lessons", "info_sub"]


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"
