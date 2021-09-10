from rest_framework.serializers import ModelSerializer
from .models import ProfilesDB


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = ProfilesDB
        fields = "__all__"
