from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Task
from .serializers import TaskSerializer

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
            serializer.save(user_id=request.user.id)
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
