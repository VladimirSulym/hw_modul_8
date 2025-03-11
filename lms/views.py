from lms.models import Course
from lms.serializers import CourseSerializer
from rest_framework import viewsets

class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet-класс для работы с моделью Course"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    # def list(self, request):
    #     # Метод для вывода списка пользователей с определением выборки из базы и указанием сериализатора
    #     queryset = Course.objects.all()
    #     serializer = CourseSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     # Метод для вывода информации по пользователю с определением выборки из базы и указанием сериализатора
    #     queryset = Course.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = CourseSerializer(user)
    #     return Response(serializer.data)
    #
    # def create(self):
    #     queryset = Course.objects.all()
    #     serializer = CourseSerializer(queryset, many=True)
    #     return Response(serializer.data)