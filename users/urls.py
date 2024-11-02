from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserTokenObtainPairView, UserViewSet, UserTokenRefreshView

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path(
        "login/",
        UserTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("token/refresh/", UserTokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
