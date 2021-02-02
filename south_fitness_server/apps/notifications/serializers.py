from rest_framework.serializers import ModelSerializer
from .models import NotificationsDB


class NotificationSerializer(ModelSerializer):

    class Meta:
        model = NotificationsDB
        fields = [
            "notification_id",
            "user_id",
            "title",
            "details",
            "viewed",
            "seen",
            "date"
        ]
