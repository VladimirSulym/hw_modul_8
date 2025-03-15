from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, permissions, generics

class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet-класс для работы с моделью Course"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям

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
