from django.urls import path
from api.views.auth import RegisterAPI, LoginAPI
from api.views.tasks import TasksAPI, TaskCreateAPI

urlpatterns = [
    path("auth/register", RegisterAPI.as_view(), name="register"),
    path("auth/login", LoginAPI.as_view(), name="login"),
    path("tasks/<int:pk>/", TasksAPI.as_view(), name="tasks"),
    path("tasks/", TaskCreateAPI.as_view(), name="tasks"),
]

