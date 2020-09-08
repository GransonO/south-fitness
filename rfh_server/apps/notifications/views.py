# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import NotificationsDB


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

# class AppointmentSpecificView(ListAPIView):
#     """Get a user specific appointments"""
#     serializer_class = AppointmentSerializer

#     def get_queryset(self):
#         return AppointmentsDB.objects.filter(
#             patientID=self.kwargs['user_id']
#             ).order_by('timestamp')


# class AppointmentGeneralView(ListAPIView):
#     """Get all users appointments"""
#     serializer_class = AppointmentSerializer

#     def get_queryset(self):
#         return AppointmentsDB.objects.filter().order_by('timestamp')
