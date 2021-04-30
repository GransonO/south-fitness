from rest_framework.serializers import ModelSerializer
from .models import MvtChallenge, JoinedClasses


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


class JoinedClassSerializer(ModelSerializer):

    class Meta:
        model = JoinedClasses
        fields = [
           "video_id",
            "user_id",
            "createdAt"
        ]
