from rest_framework.serializers import ModelSerializer
from .models import VideosDB


class SupportSerializer(ModelSerializer):

    class Meta:
        model = VideosDB
        fields = [
            "video_id",
            "uploaded_by",
            "title",
            "details",
            "video_url",
            "views_count",
            "type",
            "createdAt"
            "updatedAt"
        ]
