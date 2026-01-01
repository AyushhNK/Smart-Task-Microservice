from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Project
from .serializers import ProjectSerializer
import requests
import os

# URL of notification_service
NOTIFICATION_SERVICE_URL = os.getenv(
    "NOTIFICATION_SERVICE_URL", "http://127.0.0.1:8002/api/notifications/"
)

class ProjectListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        projects = Project.objects.filter(user_id=user_id)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user_id = request.user.id
        print(user_id)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            print(user_id)
            project = serializer.save(user_id=user_id)

            # 🔹 Send notification automatically
            try:
                headers = {
                    "Authorization": f"Bearer {request.auth}",
                    "Content-Type": "application/json",
                }
                data = {"message": f"New project created: {project.name}", "user_id": user_id}
                response = requests.post(NOTIFICATION_SERVICE_URL, json=data, headers=headers)
                if response.status_code not in [200, 201]:
                    print(f"Notification failed: {response.status_code} {response.text}")
            except Exception as e:
                print(f"Error sending notification: {e}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
