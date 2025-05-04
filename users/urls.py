from django.urls import path
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path(
        "token/",
        TokenObtainPairView.as_view(permission_classes=(permissions.AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(permissions.AllowAny,)),
        name="token_refresh",
    ),
]
