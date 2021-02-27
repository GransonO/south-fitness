from rest_framework.serializers import ModelSerializer
from .models import MvtChallenge


class ChallengeSerializer(ModelSerializer):

    class Meta:
        model = MvtChallenge
        fields = [
                "challengeId",
                "challengeType",
                "team",

                "user_id",

                "distance",
                "steps_count",
                "caloriesBurnt",
                "startTime",
                "endTime",

                "createdAt",
                "updatedAt"
        ]
