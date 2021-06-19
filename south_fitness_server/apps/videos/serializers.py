from rest_framework.serializers import ModelSerializer
from .models import VideosDB, ActivitiesDB, JoinedVidsActs


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


class ActivitySerializer(ModelSerializer):
    class Meta:
        model = ActivitiesDB
        fields = [
            "activity_id",
            "uploader_id",
            "uploaded_by",
            "title",
            "details",
            "video_url",
            "image_url",
            "type",
            "session_id",
            "duration",
            "duration_ext",
            "level",
            "equip",
            "sets",
            "isComplete",
            "createdAt",
            "updatedAt"
        ]


class JoinedClassSerializer(ModelSerializer):

    class Meta:
        model = JoinedVidsActs
        fields = [
           "activity_id",
            "user_id",
            "username",
            "user_department",
            "createdAt"
        ]
