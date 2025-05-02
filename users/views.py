from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from users.models import User
from users.serializers import UserSerialazer


class UserCreateView(CreateAPIView):
    """API-вью для создания нового пользователя"""

    serializer_class = UserSerialazer
    queryset = User.objects.all()

    permission_classes = [
        permissions.AllowAny,
    ]  # Разрешает запрос всем пользователям

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
