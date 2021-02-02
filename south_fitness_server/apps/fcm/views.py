# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .models import FcmDB
from .serializers import FcmSerializer


class FcmRecord(views.APIView):
    """
        Deal with FCM
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add FCM No to DB """
        passedData = request.data
        try:
            # Check if it exists
            result = FcmDB.objects.filter(user_id=passedData["user_id"])
            print("--------------------------------{}".format(result.count()))
            print("--------------------------------{}".format(passedData))
            if (result.count() < 1):
                # Save data to DB
                print("--------------------------------Added to DB")
                fcm_data = FcmDB(
                    token=passedData["token"],
                    user_id=passedData["user_id"],
                    platform=passedData["platform"]
                )
                fcm_data.save()
                return Response({
                    "status": "success",
                    "code": 1
                    }, status.HTTP_200_OK)
            else:
                # Update FCM
                print("--------------------------------Updated")
                FcmDB.objects.filter(user_id=passedData["user_id"]).update(
                        token=passedData["token"],
                        platform=passedData["platform"]
                    )
                return Response({
                        "status": "success",
                        "code": 1
                        }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('ProfilesRef Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)


class UserFcmRecord(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = FcmSerializer

    def get_queryset(self):
        return FcmDB.objects.filter(user_id=self.kwargs['user_id'])


class AllFcmRecords(ListAPIView):
    """Get all FCM"""
    serializer_class = FcmSerializer

    def get_queryset(self):
        return FcmDB.objects.filter().order_by('createdAt')