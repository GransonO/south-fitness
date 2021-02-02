from rest_framework.serializers import ModelSerializer
from .models import ProfilesDB


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = ProfilesDB
        fields = [
            "UserRefId",
            "birthDate",
            "chattingWith",
            "doc",
            "email",
            "firstname",
            "lastname",
            "gender",
            "userId",
            "nickname",
            "phone",
            "photoUrl",
            "relatives",
            "insurance",
            "address",
            "addressId",
            "addressName",
            "latitude",
            "longitude",
        ]
