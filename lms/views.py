from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, PaymentSerializer
from rest_framework import viewsets, permissions, generics
from django_filters.rest_framework import DjangoFilterBackend

from users.models import Payment

from rest_framework.filters import SearchFilter, OrderingFilter


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet-класс для работы с моделью Course"""
    # serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    """API-вью для создания нового урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям

class LessonListAPIView(generics.ListAPIView):
    """API-вью для получения списка всех уроков конкретного курса"""
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям
    queryset = Lesson.objects.all()

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """API-вью для получения информации о конкретном уроке"""
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям
    queryset = Lesson.objects.all()

class LessonUpdateAPIView(generics.UpdateAPIView):
    """API-вью для изменения информации о конкретном уроке"""
    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser] # Разрешает запрос только администраторам
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]  # Разрешает запрос всем пользователям
    queryset = Lesson.objects.all()

class LessonDestroyAPIView(generics.DestroyAPIView):
    """API-вью для удаления урока"""
    permission_classes = [permissions.AllowAny]  # Разрешает запрос всем пользователям
    queryset = Lesson.objects.all()

class CourseRetrieveAPIView(generics.RetrieveAPIView):
    """API-вью для получения информации о конкретном уроке"""
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям
    queryset = Course.objects.all()

class PaymentListAPIView(generics.ListAPIView):
    """API-вью для получения списка всех платежей пользователя"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.AllowAny] # Разрешает запрос только авторизованным пользователям
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['course', 'payment_type']
    ordering_fields = ['payment_date']
