from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Notification
from .serializers import NotificationSerializer
from .tasks import create_notification

class NotificationListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        notifications = Notification.objects.filter(user_id=user_id).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            create_notification.delay(request.user.id, serializer.validated_data["message"])
            return Response({"detail": "Notification queued"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
