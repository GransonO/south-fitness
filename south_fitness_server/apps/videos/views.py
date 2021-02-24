# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .models import VideosDB
from .serializers import VideoSerializer
import requests
import json


class Videos(views.APIView):
    """
        Add notifications details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add appointment to DB """
        passed_data = request.data
        try:
            # Save data to DB
            video_data = VideosDB(
                video_id=passed_data["video_id"],
                uploaded_by=passed_data["uploaded_by"],
                instructor=passed_data["instructor"],
                title=passed_data["title"],
                details=passed_data["details"],
                video_url=passed_data["video_url"],
                views_count=passed_data["views_count"],
                type=passed_data["type"],
                session_id=passed_data["session_id"]
            )
            video_data.save()
            # staffData = StaffDB.objects.filter()
            # allTokens = []
            # for x in staffData:
            #     allTokens.append(x.staffToken)
            #
            # message = "A new support has been posted"
            # Support.notifyStaff(allTokens, message)
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
    def get(request):
        pass

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
        return VideosDB.objects.filter().order_by('createdAt')


class VideoSpecificView(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = VideoSerializer

    def get_queryset(self):
        return VideosDB.objects.filter(
            video_id=self.kwargs['video_id']
            ).order_by('createdAt')
