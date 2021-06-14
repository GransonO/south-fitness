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
            "username",
            "user_department",
            "createdAt"
        ]


class ActivitiesClassSerializer(ModelSerializer):

    class Meta:
        model = JoinedClasses
        fields = [
            "activity_id",
            "title",
            "description",
            "uploaded_by",
            "image_url",
            "video_url",
            "is_active",
            "createdAt",
            "updatedAt"
        ]
