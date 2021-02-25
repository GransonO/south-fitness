from rest_framework.serializers import ModelSerializer
from .models import BlogsDB


class BlogSerializer(ModelSerializer):

    class Meta:
        model = BlogsDB
        fields = [
            "blog_id",
            "uploaded_by",
            "title",
            "body",
            "image_url",
            "views_count",
            "reading_duration",
            "updatedAt"
        ]
