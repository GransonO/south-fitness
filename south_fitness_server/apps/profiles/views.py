# Create your views here.
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
            activate = Activation.objects.filter(
                user_email=passed_data["email"],
                activation_code=int(passed_data["activation_code"])
            )
            print("------user_email : {} activation_code : {} ----------- {}".format(passed_data["email"], passed_data["activation_code"], activate.count()))
            if activate.count() < 1:
                return Response({
                    "status": "Failed",
                    "code": 0,
                    "message": "Update failed, wrong activation code passed"
                }, status.HTTP_200_OK)
            else:
                # Save data to DB
                profile_data = ProfilesDB(
                        fullname=passed_data["fullname"],
                        email=passed_data["email"],
                        # birthDate=passed_data["birthDate"],
                        activation_code=passed_data["activation_code"],
                        team=passed_data["team"].upper(),
                        # Part 2
                        gender=passed_data["gender"],
                        height=passed_data["height"],
                        weight=passed_data["weight"],
                        # Goals
                        goal=passed_data["goal"],
                        # Discipline
                        discipline=passed_data["discipline"],
                        # Work Out Duration
                        workout_duration=passed_data["workout_duration"],
                )
                profile_data.save()
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
