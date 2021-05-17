from rest_framework import serializers
from .models import BlogsDB, Comments


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = [
            "username",
            "uploader_id",
            "body",
            "profile_image",
            "updatedAt"
        ]


class BlogSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField('get_blog_comments')

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
            "comments",
            "updatedAt"
        ]

    @staticmethod
    def get_blog_comments(obj):
        return list(
                Comments.objects.filter(blog_id=obj.blog_id).values()
        )
