# Create your views here.
import random

import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .models import MvtChallenge, JoinedClasses
from .serializers import ChallengeSerializer, JoinedClassSerializer


class Challenges(views.APIView):
    """
        Add Profiles details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add Profiles to DB """
        passed_data = request.data
        try:
            # Save data to DB
            random_code = random.randint(1, 999999)
            challenge_data = MvtChallenge(
                challengeId=random_code,
                challengeType=passed_data["challengeType"],
                team=passed_data["team"],
                user_id=passed_data["user_id"],
                steps_count=passed_data["steps_count"],
                distance=passed_data["distance"],
                caloriesBurnt=passed_data["caloriesBurnt"],

            )
            challenge_data.save()
            return Response({
                "status": "success",
                "code": 1
            }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Challenge Post: {}'.format(E))
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
            participant = MvtChallenge.objects.get(user_id=passed_data["user_id"])
            serializer = ChallengeSerializer(
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


class ChallengesAllView(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        return MvtChallenge.objects.filter().order_by('createdAt')


class ChallengeSpecificView(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        return MvtChallenge.objects.filter(
            user_id=self.kwargs['user_id']
            ).order_by('createdAt')


class AllRegisteredActivities(views.APIView):
    """" Get all users challenges """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        passed_data = request.data
        try:
            # Save data to DB
            video_data = JoinedClasses(
                video_id=passed_data["video_id"],
                user_id=passed_data["user_id"],
            )
            video_data.save()

            return Response({
                "status": "success",
                "state": True,
                "code": 1
            }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Challenge Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "state": False,
                "code": 0
            }, status.HTTP_200_OK)

    @staticmethod
    def put(request):
        passed_data = request.data
        query = JoinedClasses.objects.filter(video_id=passed_data["video_id"], user_id=passed_data["user_id"],).order_by('createdAt')
        if query.count() > 0:
            # user in class
            return Response({
                "status": "success",
                "state": True,
                "code": 1
            }, status.HTTP_200_OK)
        else:
            # user Not in class
            return Response({
                "status": "success",
                "state": False,
                "code": 1
            }, status.HTTP_200_OK)


class ChallengesGetAll(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = JoinedClassSerializer

    def get_queryset(self):
        return JoinedClasses.objects.filter().order_by('createdAt')
