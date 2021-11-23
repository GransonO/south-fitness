# Create your views here.
import os
import uuid
import time
import bugsnag
from dotenv import load_dotenv
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

from .agora.RtcTokenBuilder import RtcTokenBuilder, Role_Subscriber
from .models import VideosDB, ActivitiesDB, JoinedVidsActs, VidsARatings
from .serializers import VideoSerializer, ActivitySerializer, JoinedClassSerializer
from ..challenges.models import JoinedClasses, ExtraChallenges, MvtChallenge
import requests
import json


class Videos(views.APIView):
    """ Add notifications details and save in DB """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add appointment to DB """
        video_uuid = uuid.uuid1()
        session_uuid = uuid.uuid1()
        try:
            # Save data to DB
            serializer = VideoSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(video_id=video_uuid, session_id=session_uuid)

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
        """This has been used for ratings"""
        passed_data = request.data
        try:
            rate = VidsARatings.objects.filter(activity_id=passed_data["activity_id"], user_id=passed_data["user_id"])
            if rate.count() < 1:
                rate_data = VidsARatings(
                    activity_id=passed_data["activity_id"],
                    user_id=passed_data["user_id"],
                    user_department=passed_data["user_department"],
                    username=passed_data["username"],
                    trainer_rating=passed_data["trainer_rating"],
                    activity_rating=passed_data["activity_rating"],
                )
                rate_data.save()
            return Response({
                "status": "success",
                "code": 1
            }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Rating Post: {}'.format(E))
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


class VideoUpdate(views.APIView):

    permission_classes = [AllowAny]

    @staticmethod
    def put(request):
        """Update challenge State"""
        try:
            result = VideosDB.objects.get(video_id=request.data["video_id"])
            serializer = VideoSerializer(result, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "status": "success",
                "code": 1
            }, status.HTTP_200_OK)
        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Video Put: {}'.format(E))
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

        load_dotenv()
        app_id = os.environ['SF_AGORA_APP_ID']
        app_certificate = os.environ['SF_AGORA_APP_CERTIFICATE']
        channel_name = passed_data["channel_name"]
        user_account = passed_data["username"]
        expire_time_in_seconds = 3600
        current_timestamp = int(time.time())
        privilege_expired_ts = current_timestamp + expire_time_in_seconds

        print("----------------------------- {}".format(passed_data["can_start"]))

        if passed_data["can_start"] is True:
            # Started by trainer
            token = RtcTokenBuilder.buildTokenWithUid(
                app_id, app_certificate, channel_name, user_account, Role_Subscriber, privilege_expired_ts)

            VideosDB.objects.filter(
                video_id=passed_data["video_id"]).update(
                video_call_id=app_id,
                video_call_token=token,
                video_channel_name=channel_name,
                isLive=True
            )
            return Response({'token': token, 'appID': app_id}, status.HTTP_200_OK)
        else:
            token = RtcTokenBuilder.buildTokenWithUid(
                app_id, app_certificate, channel_name, user_account, Role_Subscriber, privilege_expired_ts)

            result = VideosDB.objects.filter(video_id=passed_data["video_id"])
            video_list = list(result)
            print("----------------------------- {}".format(video_list[0].isLive))
            return Response({'token': token, 'appID': app_id, 'isStarted': video_list[0].isLive}, status.HTTP_200_OK)


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

        activity_uuid = uuid.uuid1()
        session_uuid = uuid.uuid1()
        try:
            # Save data to DB
            serializer = ActivitySerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(activity_id=activity_uuid, session_id=session_uuid)
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
            # Check if user in class
            is_in_class = JoinedVidsActs.objects.filter(
                activity_id=passed_data["activity_id"],
                user_id=passed_data["user_id"])

            if is_in_class.count() < 1:
                # Save data to DB
                serializer = JoinedClassSerializer(data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

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


class ActivityUpdate(views.APIView):

    permission_classes = [AllowAny]

    @staticmethod
    def put(request):
        """Update challenge State"""
        try:
            result = ActivitiesDB.objects.get(activity_id=request.data["activity_id"])
            serializer = ActivitySerializer(result, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "status": "success",
                "code": 1
            }, status.HTTP_200_OK)
        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Video Put: {}'.format(E))
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
            activity_id=self.kwargs['activity_id']
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


class History(views.APIView):
    """Get all user activities"""
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        # get Activities from
        vids_acts_list = []
        joined_classes = []
        daily_challenges = []
        passed_data = request.data

        # JoinedVidsActs videos
        try:
            vids_acts = JoinedVidsActs.objects.filter(
                createdAt__range=[passed_data["date_from"], passed_data["date_to"]], user_id=passed_data["user_id"])
            vids_list = list(vids_acts)
            for item in vids_list:
                # for videos only
                vids = VideosDB.objects.filter(video_id=item.activity_id)
                if vids.count() > 0:
                    list_item = list(vids)
                    vids_acts_list.append({
                        "activity_id": list_item[0].video_id,
                        "title": list_item[0].title,
                        "image_url": list_item[0].image_url,
                        "type": list_item[0].type,
                        "points": list_item[0].points
                    })

                # Activities
                acts = ActivitiesDB.objects.filter(activity_id=item.activity_id)
                if acts.count() > 0:
                    list_item = list(acts)
                    vids_acts_list.append({
                        "activity_id": list_item[0].activity_id,
                        "title": list_item[0].title,
                        "image_url": list_item[0].image_url,
                        "type": list_item[0].type,
                        "points": list_item[0].points
                    })

            # JoinedClasses Challenges
            joined_list = JoinedClasses.objects.filter(
                createdAt__range=[passed_data["date_from"], passed_data["date_to"]], user_id=passed_data["user_id"])
            for item in joined_list:
                # for videos only
                vids = ExtraChallenges.objects.filter(challenge_id=item.challenge_id)
                if vids.count() > 0:
                    list_item = list(vids)
                    joined_classes.append({
                        "activity_id": list_item[0].challenge_id,
                        "title": list_item[0].title,
                        "image_url": list_item[0].image_url,
                        "type": list_item[0].type,
                        "points": list_item[0].points
                    })

            # Daily Challenges
            daily_list = MvtChallenge.objects.filter(
                createdAt__range=[passed_data["date_from"], passed_data["date_to"]], user_id=passed_data["user_id"])
            for item in daily_list:
                image_url = ""
                # for daily_challenges only
                if item.challengeType == "Cycling":
                    image_url = "https://res.cloudinary.com/dolwj4vkq/image/upload/v1620142203/South_Fitness/bike.jpg"
                elif item.challengeType == "Running":
                    image_url = "https://res.cloudinary.com/dolwj4vkq/image/upload/v1620141989/South_Fitness/runner.jpg"
                elif item.challengeType == "Walking":
                    image_url = "https://res.cloudinary.com/dolwj4vkq/image/upload/v1620142299/South_Fitness/walking.jpg"

                joined_classes.append({
                    "activity_id": item.challengeId,
                    "title": "Daily {} challenge".format(item.challengeType),
                    "image_url": image_url,
                    "type": item.challengeType,
                    "points": 20  # Default for daily challenges
                })

            final_list = vids_acts_list + joined_classes + daily_challenges

            return Response({
                "status": "success",
                "history_list": final_list
            }, status.HTTP_200_OK)
        except Exception as E:
            bugsnag.notify(
                Exception('History Pull: {}'.format(E))
            )
            return Response({
                "status": "fail"
            }, status.HTTP_200_OK)
