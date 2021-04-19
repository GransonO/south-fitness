from rest_framework.serializers import ModelSerializer
from .models import ProfilesDB


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = ProfilesDB
        fields = [
            "fullname", "email", "birthDate", "activation_code", "team", "image", "gender", "height",
            "user_id", "weight", "goal", "discipline", "workout_duration", "user_type", "institution"
        ]
