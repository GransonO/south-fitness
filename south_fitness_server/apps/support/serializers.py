from rest_framework.serializers import ModelSerializer
from .models import SupportDB


class SupportSerializer(ModelSerializer):

    class Meta:
        model = SupportDB
        fields = [
            "support_id",
            "user_id",
            "title",
            "details",
            "image",
            "response",
            "tracker",
            "dateTime",
            "updatedAt"
        ]
