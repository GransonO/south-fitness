# Create your views here.
import uuid
import time
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

from .agora.RtcTokenBuilder import RtcTokenBuilder, Role_Subscriber
from .models import VideosDB, ActivitiesDB, JoinedVidsActs
from .serializers import VideoSerializer, ActivitySerializer
import requests
import json


class Videos(views.APIView):
    """ Add notifications details and save in DB """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add appointment to DB """
        passed_data = request.data

        video_uuid = uuid.uuid1()
        session_uuid = uuid.uuid1()
        try:
            # Save data to DB
            video_data = VideosDB(
                video_id=video_uuid,
                uploaded_by=passed_data["uploaded_by"],
                instructor=passed_data["instructor"],
                uploader_id=passed_data["uploader_id"],
                title=passed_data["title"],
                details=passed_data["details"],
                video_url=passed_data["video_url"],
                type=passed_data["type"],
                session_id=session_uuid,
                isScheduled=passed_data["isScheduled"],
                image_url=passed_data["image_url"],
                duration=passed_data["duration"],
                scheduledTime=passed_data["scheduledTime"],
                scheduledDate=passed_data["scheduledDate"]
            )
            video_data.save()

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
    def notify_staff(all_tokens, message):
        """Send notification to the doctor"""
        url = 'https://fcm.googleapis.com/fcm/send'

        myHeaders = {
            "Authorization": "key=AAAAxTAONtw:APA91bHOkfYKzBkGvUj4NMzK8JTaWHDwf8g_GAxDeMPvijZ2IdWu3C1mjdsIRSKl1c8oBaGP4C7YSrSsJ-H09zofTepJEREMu7-8KTV5oSK9lqlBoCtyNb8wDJIHBG7IHkQXC4V3dbRU",
            "content-type": "application/json"
            }

        messageBody = {
            "title": "New support",
            "text": message,
            "icon": "https://res.cloudinary.com/dolwj4vkq/image/upload/v1578849920/RFH/RFH-colored-white-icon.png",
        }

        myData = {
            "registration_ids": all_tokens,
            "notification": messageBody,
        }

        x = requests.post(url, headers=myHeaders, data=json.dumps(myData))
        print("message sent : {}".format(x))

    @staticmethod
    def put(request):
        passedData = request.data
        try:
            vid_data = VideosDB.objects.get(video_id=passedData["video_id"])

            VideosDB.objects.filter(
                video_id=passedData["video_id"]).update(
                    views_count=vid_data.views_count + 1,
                    participants="{},{}".format(vid_data.participants, passedData["team"].upper())
                    )
            return Response({
                    "status": "success",
                    "code": 1
                    }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Update Videos count: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)


class VideoAllView(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = VideoSerializer

    def get_queryset(self):
        return VideosDB.objects.filter(scheduledDate__gt=self.kwargs["yester_date"]).order_by('-createdAt')


class VideoAdmin(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = VideoSerializer

    def get_queryset(self):
        return VideosDB.objects.filter().order_by('-createdAt')


class VideoSpecificView(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = VideoSerializer

    def get_queryset(self):
        return VideosDB.objects.filter(
            video_id=self.kwargs['video_id']
            ).order_by('createdAt')


class VideoTrainerSpecific(ListAPIView):
    """Get a trainer specific"""
    permission_classes = [AllowAny]
    serializer_class = VideoSerializer

    def get_queryset(self):
        return VideosDB.objects.filter(
            uploader_id=self.kwargs['uploader_id']
            ).order_by('-createdAt')


class TokenGenerator(views.APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        passed_data = request.data
        app_id = 'ecfc8ba2d43744588161f36ff1c71cfc'
        app_certificate = '8c5f930076ca44108b93099d06020376'
        channel_name = passed_data["channel_name"]
        user_account = passed_data["username"]
        expire_time_in_seconds = 3600
        current_timestamp = int(time.time())
        privilege_expired_ts = current_timestamp + expire_time_in_seconds

        token = RtcTokenBuilder.buildTokenWithUid(
            app_id, app_certificate, channel_name, user_account, Role_Subscriber, privilege_expired_ts)

        VideosDB.objects.filter(
            video_id=passed_data["video_id"]).update(
            video_call_id=app_id,
            video_call_token=token,
            video_channel_name=channel_name
        )
        return Response({'token': token, 'appID': app_id}, status.HTTP_200_OK)


class DateRequest(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = VideoSerializer

    def get_queryset(self):
        return VideosDB.objects.filter(scheduledDate=self.kwargs['date']).order_by('createdAt')

# ACTIVITIES


class Activities(views.APIView):
    """ Add notifications details and save in DB """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add appointment to DB """
        passed_data = request.data

        activity_uuid = uuid.uuid1()
        session_uuid = uuid.uuid1()
        try:
            # Save data to DB
            activity_data = ActivitiesDB(
                activity_id=activity_uuid,
                uploaded_by=passed_data["uploaded_by"],
                uploader_id=passed_data["uploader_id"],
                title=passed_data["title"],
                details=passed_data["details"],
                video_url=passed_data["video_url"],
                image_url=passed_data["image_url"],
                type=passed_data["type"],
                session_id=session_uuid,
                duration=passed_data["duration"],
                duration_ext=passed_data["duration_ext"],
                level=passed_data["level"],
                equip=passed_data["equip"],
                isComplete=passed_data["isComplete"],
            )
            activity_data.save()

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
    def notify_staff(all_tokens, message):
        """Send notification to the doctor"""
        url = 'https://fcm.googleapis.com/fcm/send'

        myHeaders = {
            "Authorization": "key=AAAAxTAONtw:APA91bHOkfYKzBkGvUj4NMzK8JTaWHDwf8g_GAxDeMPvijZ2IdWu3C1mjdsIRSKl1c8oBaGP4C7YSrSsJ-H09zofTepJEREMu7-8KTV5oSK9lqlBoCtyNb8wDJIHBG7IHkQXC4V3dbRU",
            "content-type": "application/json"
            }

        messageBody = {
            "title": "New support",
            "text": message,
            "icon": "https://res.cloudinary.com/dolwj4vkq/image/upload/v1578849920/RFH/RFH-colored-white-icon.png",
        }

        myData = {
            "registration_ids": all_tokens,
            "notification": messageBody,
        }

        x = requests.post(url, headers=myHeaders, data=json.dumps(myData))
        print("message sent : {}".format(x))

    @staticmethod
    def put(request):
        # Member joining activity
        passed_data = request.data

        try:
            # Save data to DB
            joined_data = JoinedVidsActs(
                activity_id=passed_data["activity_id"],
                user_id=passed_data["user_id"],
                user_department=passed_data["user_department"],
                username=passed_data["username"],
            )
            joined_data.save()

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


class ActivitiesAllView(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return ActivitiesDB.objects.filter(isComplete=False).order_by('-createdAt')


class ActivitiesAdmin(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return ActivitiesDB.objects.filter().order_by('-createdAt')


class ActivitiesSpecificView(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return ActivitiesDB.objects.filter(
            video_id=self.kwargs['video_id']
            ).order_by('createdAt')


class ActivitiesTrainerSpecific(ListAPIView):
    """Get a trainer specific"""
    permission_classes = [AllowAny]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return ActivitiesDB.objects.filter(
            uploader_id=self.kwargs['uploader_id']
            ).order_by('-createdAt')


class Participants(views.APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        passed_data = request.data

        members = JoinedVidsActs.objects.filter(activity_id=passed_data["activity_id"])
        members_list = list(members)
        new_list = []
        dep_list = []
        for member in members_list:
            dep_list.append(
                member.user_department
            )
            new_list.append(
                {
                    "activity_id": member.activity_id,
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
    def get(request):
        members = JoinedVidsActs.objects.filter()
        members_list = list(members)
        new_list = []
        dep_list = []
        for member in members_list:
            dep_list.append(
                member.user_department
            )
            new_list.append(
                {
                    "activity_id": member.activity_id,
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
        members = JoinedVidsActs.objects.filter(user_department=passed_data["user_department"])
        members_list = list(members)
        new_list = []
        user_list = []
        for member in members_list:
            user_list.append(
                member.username
            )
            new_list.append(
                {
                    "activity_id": member.activity_id,
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
