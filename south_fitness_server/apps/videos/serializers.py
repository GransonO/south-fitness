from rest_framework.serializers import ModelSerializer
from .models import VideosDB


class VideoSerializer(ModelSerializer):

    class Meta:
        model = VideosDB
        fields = [
            "video_id",
            "uploader_id",
            "uploaded_by",
            "instructor",
            "title",
            "details",
            "video_url",
            "image_url",
            "views_count",
            "type",
            "session_id",
            "isScheduled",
            "duration",
            "scheduledDate",
            "scheduledTime",
            "isComplete",
            "isLive",
            "participants",
            "video_call_id",
            "video_call_token",
            "video_channel_name",
            "createdAt",
            "updatedAt"
        ]
