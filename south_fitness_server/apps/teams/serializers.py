from rest_framework.serializers import ModelSerializer
from .models import TeamsDB


class TeamsSerializer(ModelSerializer):

    class Meta:
        model = TeamsDB
        fields = [
            "teams_id",
            "team_name",
            "slogan",
            "image",
            "created_by",
            "is_active",
            "updatedAt",
            "createdAt"
        ]
