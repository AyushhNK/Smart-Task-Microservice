from django.urls import path
from .views import NotificationListCreateAPIView

urlpatterns = [
    path("notifications/", NotificationListCreateAPIView.as_view(), name="notifications-list-create"),
]
