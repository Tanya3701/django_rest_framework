from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, \
    UserDestroyAPIView

app_name = UsersConfig.name


urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment_list"),
    path("users/create/", UserCreateAPIView.as_view(), name="user_create"),
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path(
        "users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"
    ),
    path(
        "users/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user_delete"
    ),
    path(
        "login/",
        TokenObtainPairView.as_view(
            permission_classes=(AllowAny,),
        ),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
