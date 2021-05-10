from rest_framework import serializers
from .models import BlogsDB, Comments


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
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


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = [
            "blog_id",
            "username",
            "uploader_id",
            "body",
            "profile_image",
            "updatedAt"
        ]
