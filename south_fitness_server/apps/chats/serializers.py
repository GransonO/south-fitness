from rest_framework.serializers import ModelSerializer
from .models import ChatDB
from .models import GroupsDB


class ChatSerializer(ModelSerializer):

    class Meta:
        model = ChatDB
        fields = [
                "message_id",
                "group_id",
                "user_id",
                "message",
                "reply_body",
                "username",
                "createdAt"
        ]


class GroupSerializer(ModelSerializer):

    class Meta:
        model = GroupsDB
        fields = [
                "group_id",
                "created_by",
                "group_title",
                "creator_name",
                "group_slogan",
                "channel_id",
                "createdAt",
        ]
