# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from django.db.models import Q
from .models import NotificationsDB
from .serializers import NotificationSerializer


class Notifications(views.APIView):
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
            notifications_data = NotificationsDB(
                notification_id=passedData["notification_id"],
                user_id=passedData["user_id"],
                title=passedData["title"],
                details=passedData["details"],
                viewed=passedData["viewed"]
            )
            notifications_data.save()
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
            updateColumn = NotificationsDB.objects.get(
                notification_id=passedData["notification_id"]
                )

            totalViews = updateColumn.viewed + 1
            NotificationsDB.objects.filter(
                notification_id=passedData["notification_id"]).update(
                        viewed=totalViews,
                        seen=True
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


class NotificationAllView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return NotificationsDB.objects.filter().order_by('date')


class NotificationSpecificView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return NotificationsDB.objects.filter(
            notification_id=self.kwargs['notification_id']
            ).order_by('date')


class NotificationUserView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = NotificationSerializer

    def get_queryset(self):
        criterion1 = Q(user_id__contains=self.kwargs['user_id'])
        criterion2 = Q(user_id__contains="all")
        return NotificationsDB.objects.filter(
            criterion1 | criterion2
            ).order_by('date')


# class AppointmentGeneralView(ListAPIView):
#     """Get all users appointments"""
#     serializer_class = AppointmentSerializer

#     def get_queryset(self):
#         return AppointmentsDB.objects.filter().order_by('timestamp')
