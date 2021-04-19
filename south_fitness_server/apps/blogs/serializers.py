from rest_framework.serializers import ModelSerializer
from .models import BlogsDB


class BlogSerializer(ModelSerializer):

    class Meta:
        model = BlogsDB
        fields = [
            "blog_id",
            "uploaded_by",
            "uploader_id",
            "title",
            "body",
            "uploader_id",
            "image_url",
            "views_count",
            "reading_duration",
            "likes_count",
            "comments_count",
            "updatedAt"
        ]
