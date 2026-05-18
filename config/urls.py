from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("lessons/", include("lessons.urls", namespace="lessons")),
    path("users/", include("users.urls", namespace="users")),
]
