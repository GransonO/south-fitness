from rest_framework.serializers import ModelSerializer
from .models import MvtChallenge, ExtraChallenges


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


class ExtraChallengeSerializer(ModelSerializer):

    class Meta:
        model = ExtraChallenges
        fields = [
            "challenge_id",
            "uploaded_by",
            "uploader_id",
            "title",
            "details",
            "video_url",
            "image_url",
            "type",
            "session_id",
            "isComplete",
            "level",
            "duration",
            "duration_ext"
        ]
