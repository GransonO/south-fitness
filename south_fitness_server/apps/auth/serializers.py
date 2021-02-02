from rest_framework.serializers import ModelSerializer
from .models import FcmDB


class FcmSerializer(ModelSerializer):

    class Meta:
        model = FcmDB
        fields = [
            "token",
            "user_id"
        ]
