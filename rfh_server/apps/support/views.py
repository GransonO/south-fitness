# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from django.db.models import Q
from .models import SupportDB
from .serializers import SupportSerializer


class Support(views.APIView):
    """
        Add notifications details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add appointment to DB """
        passedData = request.data
        try:
            # Save data to DB
            support_data = SupportDB(
                support_id=passedData["support_id"],
                user_id=passedData["user_id"],
                title=passedData["title"],
                details=passedData["details"],
                image=passedData["image"],
                response=passedData["response"],
                tracker=passedData["tracker"]
            )
            support_data.save()
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
    def get(request):
        passed_data = request.data
        print("The passedData is ------------------: {}".format(passed_data))
        return Response({"Hit the appointments channel"}, status.HTTP_200_OK)

    @staticmethod
    def put(request):
        passedData = request.data
        try:
            SupportDB.objects.filter(
                support_id=passedData["support_id"]).update(
                        response=passedData["response"],
                    )
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


class SupportAllView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = SupportSerializer

    def get_queryset(self):
        return SupportDB.objects.filter().order_by('dateTime')


class SupportSpecificView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = SupportSerializer

    def get_queryset(self):
        return SupportDB.objects.filter(
            notification_id=self.kwargs['support_id']
            ).order_by('dateTime')


class SupportUserView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = SupportSerializer

    def get_queryset(self):
        criterion = Q(user_id__contains=self.kwargs['user_id'])
        return SupportDB.objects.filter(criterion).order_by('dateTime')
