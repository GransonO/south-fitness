# Create your views here.
from datetime import datetime
import uuid

import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .models import MvtChallenge, JoinedClasses, ExtraChallenges
from .serializers import ChallengeSerializer, ExtraChallengeSerializer


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
            challenge_data = MvtChallenge(
                challengeId=uuid.uuid1(),
                challengeType=passed_data["challengeType"],
                team=passed_data["team"],
                user_id=passed_data["user_id"],
                startTime=datetime.strptime(passed_data["startTime"], '%Y-%m-%d %H:%M:%S').date(),
                steps_count=passed_data["steps_count"],
                distance=passed_data["distance"],
                caloriesBurnt=passed_data["caloriesBurnt"],
                start_latitude=passed_data["startLat"],
                start_longitude=passed_data["startLong"],
                end_latitude=passed_data["endLat"],
                end_longitude=passed_data["endLong"],
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


class TodayChallenges(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        current_date = "{}-{}-{} 00:01:00".format(
            datetime.now().year,
            datetime.now().month,
            datetime.now().day
        )

        now_date = "{}-{}-{} 23:00:00".format(
            datetime.now().year,
            datetime.now().month,
            datetime.now().day,
        )
        return MvtChallenge.objects.filter(
            createdAt__range=[current_date, now_date],
            user_id=self.kwargs["user_id"]
        ).order_by('createdAt')


class Participants(views.APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        passed_data = request.data
        members = JoinedClasses.objects.filter(challenge_id=passed_data["challenge_id"])
        members_list = list(members)
        new_list = []
        dep_list = []
        for member in members_list:
            dep_list.append(
                member.user_department
            )
            new_list.append(
                {
                    "challenge_id": member.challenge_id,
                    "user_id": member.user_id,
                    "user_department": member.user_department,
                }
            )
        dep_list = list(dict.fromkeys(dep_list))
        result_list = []

        for item in dep_list:
            item_count = 0
            for x in new_list:
                if x["user_department"] == item:
                    item_count = item_count + 1

            result_list.append(
                {
                    "name": item,
                    "count": item_count
                }
            )

        return Response({
            "status": "success",
            "members_list": sorted(result_list, key=lambda k: k['count'], reverse=True)
        }, status.HTTP_200_OK)

    @staticmethod
    def get():
        members = JoinedClasses.objects.filter()
        members_list = list(members)
        new_list = []
        dep_list = []
        for member in members_list:
            dep_list.append(
                member.user_department
            )
            new_list.append(
                {
                    "challenge_id": member.challenge_id,
                    "user_id": member.user_id,
                    "user_department": member.user_department,
                }
            )
        dep_list = list(dict.fromkeys(dep_list))
        result_list = []

        for item in dep_list:
            item_count = 0
            for x in new_list:
                if x["user_department"] == item:
                    item_count = item_count + 1

            result_list.append(
                {
                    "name": item,
                    "count": item_count
                }
            )

        return Response({
            "status": "success",
            "members_list": sorted(result_list, key=lambda k: k['count'], reverse=True)
        }, status.HTTP_200_OK)

    @staticmethod
    def put(request):
        passed_data = request.data
        members = JoinedClasses.objects.filter(user_department=passed_data["user_department"])
        members_list = list(members)
        new_list = []
        user_list = []
        for member in members_list:
            user_list.append(
                member.username
            )
            new_list.append(
                {
                    "challenge_id": member.challenge_id,
                    "user_id": member.user_id,
                    "user_department": member.user_department,
                    "username": member.username,
                }
            )
        user_list = list(dict.fromkeys(user_list))
        result_list = []

        for item in user_list:
            item_count = 0
            for x in new_list:
                if x["username"] == item:
                    item_count = item_count + 1

            result_list.append(
                {
                    "name": item,
                    "count": item_count
                }
            )

        return Response({
            "status": "success",
            "team": passed_data["user_department"],
            "members_list": sorted(result_list, key=lambda k: k['count'], reverse=True)
        }, status.HTTP_200_OK)


class ListedChallenge(views.APIView):
    """Posting general challenges"""
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add appointment to DB """
        passed_data = request.data

        challenge_id = uuid.uuid1()
        session_uuid = uuid.uuid1()
        try:
            # Save data to DB
            extra_data = ExtraChallenges(
                challenge_id=challenge_id,
                uploaded_by=passed_data["uploaded_by"],
                uploader_id=passed_data["uploader_id"],
                title=passed_data["title"],
                details=passed_data["details"],
                video_url=passed_data["video_url"],
                type=passed_data["type"],
                session_id=session_uuid,
                level=passed_data["level"],
                image_url=passed_data["image_url"],
                duration=passed_data["duration"],
                duration_ext=passed_data["duration_ext"]
            )
            extra_data.save()

            return Response({
                "status": "success",
                "code": 1
                }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Video Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)

    @staticmethod
    def put(request):
        """Update challenge State"""
        try:
            result = ExtraChallenges.objects.filter(challenge_id=request.data["challenge_id"])
            if result.count() > 0:
                ExtraChallenges.objects.filter(
                    challenge_id=request.data["challenge_id"]).update(
                    isComplete=request.data["isComplete"])
                return Response({
                    "status": "success",
                    "code": 1
                }, status.HTTP_200_OK)
        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('ExtraChallenges Put: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)


class GetListedChallenge(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = ExtraChallengeSerializer

    def get_queryset(self):

        return ExtraChallenges.objects.filter().order_by('createdAt')
