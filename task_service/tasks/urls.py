from django.urls import path
from .views import TaskListCreateAPIView, TaskDetailAPIView

urlpatterns = [
    path("tasks/", TaskListCreateAPIView.as_view()),
    path("tasks/<int:task_id>/", TaskDetailAPIView.as_view()),
    
]
