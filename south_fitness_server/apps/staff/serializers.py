from rest_framework.serializers import ModelSerializer
from .models import StaffDB


class StaffSerializer(ModelSerializer):

    class Meta:
        model = StaffDB
        fields = [
            "enabled",
            "isAdmin",
            "hospitalID",
            "staffID",
            "staffEmail",
            "staffName",
            "staffImage",
            "staffDepartment",
            "staffPhone",
            "onlineStatus",
            "lastLoggedIn",
            "currentlyOnCall",
            "staffGender",
            "staffToken",
            "createdAt"
        ]
