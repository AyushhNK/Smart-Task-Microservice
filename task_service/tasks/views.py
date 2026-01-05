from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Task
from .serializers import TaskSerializer
import requests
import os
from .kafka_producer import send_task_notification

# URL of notification_service
NOTIFICATION_SERVICE_URL = os.getenv(
    "NOTIFICATION_SERVICE_URL", "http://127.0.0.1:8002/api/notifications/"
)


class TaskListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user_id=request.user.id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(type(request.user))
        print(request.user)
        print(request.user.id)

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task=serializer.save(user_id=request.user.id)
            try:
                headers = {
                    "Authorization": f"Bearer {request.auth}",  # forward JWT
                    "Content-Type": "application/json",
                }
                data = {"message": f"New task assigned: {task.title}","user_id": request.user.id}

                response = requests.post(NOTIFICATION_SERVICE_URL, json=data, headers=headers)
                if response.status_code not in [200, 201]:
                    print(f"Notification failed: {response.status_code} {response.text}")
            except Exception as e:
                print(f"Error sending notification: {e}")
            send_task_notification(task.title, request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, task_id, user_id):
        return Task.objects.get(id=task_id, user_id=user_id)

    def get(self, request, task_id):
        try:
            task = self.get_object(task_id, request.user.id)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, task_id):
        try:
            task = self.get_object(task_id, request.user.id)
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, task_id):
        try:
            task = self.get_object(task_id, request.user.id)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
