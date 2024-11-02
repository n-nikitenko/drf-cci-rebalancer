from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer,
                                                  TokenRefreshSerializer)
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.forms import UserAuthForm
from users.models import User
from users.serializers import UserUpdateSerializer, UserSerializer


class UserTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        tags=["Аутентификация"],
        operation_description="Получение токена. Этот эндпоинт позволяет получить JWT токен на "
                              "основе учетных данных пользователя.",
        responses={
            200: openapi.Response("Успех", TokenObtainPairSerializer),
            401: "Неверные учетные данные",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        tags=["Аутентификация"],
        operation_description="Обновление токена. Этот эндпоинт позволяет обновить JWT токен, предоставленный ранее.",
        responses={
            200: openapi.Response("Успех", TokenRefreshSerializer),
            401: "Токен недействителен",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Получение списка пользователей", tags=["Пользователи"]
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Регистрация пользователя", tags=["Пользователи"]
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Получение данных пользователя по id", tags=["Пользователи"]
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Обновление данных пользователя по id", tags=["Пользователи"]
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Обновление данных пользователя по id", tags=["Пользователи"]
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Удаление данных пользователя по id", tags=["Пользователи"]
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                AllowAny,
            )
        else:
            self.permission_classes = (
                IsAuthenticated,
            )
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class AdminLoginView(LoginView):
    form_class = UserAuthForm
    template_name = 'admin/login.html'
