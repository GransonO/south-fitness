# Create your views here.
import uuid

import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .models import ProfilesDB
from .serializers import ProfileSerializer
from ..authentication.models import Activation


class Profiles(views.APIView):
    """
        Add Profiles details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add Profiles to DB """
        passed_data = request.data
        try:
            user_profile = ProfilesDB.objects.filter(
                email=passed_data["email"],
                activation_code=int(passed_data["activation_code"])
            )
            if user_profile.count() < 1:
                return Response({
                    "status": "Failed",
                    "code": 0,
                    "message": "Update failed, user not found"
                }, status.HTTP_200_OK)
            else:
                active_profile = ProfilesDB.objects.get(
                    email=passed_data["email"],
                    activation_code=int(passed_data["activation_code"])
                )
                # Save data to DB
                profile_data = ProfileSerializer(
                    active_profile, passed_data, partial=True
                )
                profile_data.is_valid()
                profile_data.save(is_active=True)
                return Response({
                    "status": "success",
                    "user_id": user_profile[0].user_id,
                    "code": 1
                    }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Profile Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)

    @staticmethod
    def put(request):
        passed_data = request.data
        # Check This later
        try:
            participant = ProfilesDB.objects.get(email=passed_data["email"])
            serializer = ProfileSerializer(
                participant, data=passed_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                    "status": "success",
                    "code": 1
                    }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Profile Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)


class CodeVerify(views.APIView):
    """Verify User code"""
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add Profiles to DB """
        passed_data = request.data
        try:
            activate = Activation.objects.filter(
                user_email=passed_data["email"],
                activation_code=int(passed_data["activation_code"])
            )
            if activate.count() < 1:
                return Response({
                    "status": "Failed",
                    "code": 0,
                    "message": "Update failed, wrong activation code passed"
                }, status.HTTP_200_OK)
            else:
                return Response({
                    "status": "success",
                    "code": 1
                    }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Appointment Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)


class ProfilesAllView(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return ProfilesDB.objects.filter().order_by('createdAt')


class ProfileSpecificView(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return ProfilesDB.objects.filter(
            email=self.kwargs['email']
            ).order_by('createdAt')


class ProfileInstitutionSpecific(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return ProfilesDB.objects.filter(
            institution_id=self.kwargs['institution']
            ).order_by('createdAt')
