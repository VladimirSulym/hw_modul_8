from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from lms.models import Course, Lesson, Payment
from lms.permissions import IsModerators, IsOwner
from lms.serializers import (
    CourseDetailSerializer,
    CourseSerializer,
    LessonSerializer,
    PaymentSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet-класс для работы с моделью Course"""

    # serializer_class = CourseSerializer
    queryset = Course.objects.all()
    # permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                ~IsModerators,
                permissions.IsAuthenticated,
            )
        elif self.action in [
            "update",
            "retrieve",
        ]:
            self.permission_classes = (
                IsModerators | IsOwner,
                permissions.IsAuthenticated,
            )
        elif self.action == "delete":
            self.permission_classes = (
                ~IsModerators,
                permissions.IsAuthenticated,
                IsOwner,
            )
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    """API-вью для создания нового урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям
    permission_classes = [
        ~IsModerators,
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """API-вью для получения списка всех уроков конкретного курса"""

    serializer_class = LessonSerializer
    # permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """API-вью для получения информации о конкретном уроке"""

    serializer_class = LessonSerializer
    # permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям
    queryset = Lesson.objects.all()
    permission_classes = (
        IsModerators | IsOwner,
        permissions.IsAuthenticated,
    )


class LessonUpdateAPIView(generics.UpdateAPIView):
    """API-вью для изменения информации о конкретном уроке"""

    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser] # Разрешает запрос только администраторам
    serializer_class = LessonSerializer
    # permission_classes = [permissions.AllowAny]  # Разрешает запрос всем пользователям
    queryset = Lesson.objects.all()
    permission_classes = (
        IsModerators | IsOwner,
        permissions.IsAuthenticated,
    )


class LessonDestroyAPIView(generics.DestroyAPIView):
    """API-вью для удаления урока"""

    # permission_classes = [permissions.AllowAny]  # Разрешает запрос всем пользователям
    queryset = Lesson.objects.all()
    permission_classes = (
        ~IsModerators,
        permissions.IsAuthenticated,
        IsOwner,
    )


class CourseRetrieveAPIView(generics.RetrieveAPIView):
    """API-вью для получения информации о конкретном уроке"""

    serializer_class = CourseDetailSerializer
    # permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям
    queryset = Course.objects.all()
    permission_classes = (
        IsModerators | IsOwner,
        permissions.IsAuthenticated,
    )


class PaymentListAPIView(generics.ListAPIView):
    """API-вью для получения списка всех платежей пользователя"""

    serializer_class = PaymentSerializer
    # permission_classes = [permissions.AllowAny] # Разрешает запрос только авторизованным пользователям
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
    search_fields = [
        "amount",
    ]
    filterset_fields = ["course", "payment_type"]
    ordering_fields = ["payment_date"]
