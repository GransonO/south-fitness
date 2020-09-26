# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import AppointmentsDB
from ..staff.models import StaffDB
from rest_framework.generics import ListAPIView
from .serializers import AppointmentSerializer
from django.db.models import Q
from django.utils import timezone
import requests
import json


class AppointmentsViews(views.APIView):
    """
        Pick all MPESA details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add appointment to DB """
        passedData = request.data
        try:
            # Save data to DB
            appointment_data = AppointmentsDB(
                doctorID=passedData["doctorID"],
                doctorName=passedData["doctorName"],
                stateColor=passedData["state_color"],
                status=passedData["status"],
                dateString=passedData["date"],
                timeString=passedData["time"],
                hospitalID=passedData["hospital_id"],
                hospitalPhone=passedData["hospital_phone"],
                hospitalName=passedData["center"],
                appointmentID=passedData["id"],
                patientID=passedData["patient_id"],
                paymentType=passedData["paymentType"],
                patientPhone=passedData["phone_no"],
                appointmentState=passedData["state"],
                summary=passedData["summary"],
                appointmentType=passedData["type"],
                timestamp=passedData["timeStamp"],
            )
            appointment_data.save()
            staffData = StaffDB.objects.filter()
            allTokens = []
            for x in staffData:
                allTokens.append(x.staffToken)

            apType = "General"
            if(passedData["type"] == 2):
                apType = "Online"

            message = "A new {} appointment has been posted".format(apType)

            AppointmentsViews.notifyStaff(allTokens, message)
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

    def notifyStaff(allTokens, message):
        """Send notification to the doctor"""
        url = 'https://fcm.googleapis.com/fcm/send'

        myHeaders = {
            "Authorization": "key=AAAAxTAONtw:APA91bHOkfYKzBkGvUj4NMzK8JTaWHDwf8g_GAxDeMPvijZ2IdWu3C1mjdsIRSKl1c8oBaGP4C7YSrSsJ-H09zofTepJEREMu7-8KTV5oSK9lqlBoCtyNb8wDJIHBG7IHkQXC4V3dbRU",
            "content-type": "application/json"
            }

        messageBody = {
            "title": "New Appointment",
            "text": message,
            "icon": "https://res.cloudinary.com/dolwj4vkq/image/upload/v1578849920/RFH/RFH-colored-white-icon.png",
        }

        myData = {
            "registration_ids": allTokens,
            "notification": messageBody,
        }

        x = requests.post(url, headers=myHeaders, data=json.dumps(myData))
        print("message sent : {}".format(x))

    @staticmethod
    def put(request):
        """Get the Mpesa value deposited"""
        passedData = request.data
        try:
            result = AppointmentsDB.objects.get(
                appointmentID=passedData["appointmentID"])
            serializer = AppointmentSerializer(
                result, data=passedData, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                    "status": "success",
                    "code": 1
                    }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Transaction Put: {}'.format(E))
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


class AppointmentState(views.APIView):
    """
        Get appointments status
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Check if appointment is full """
        passedData = request.data
        # Check if these parameters are passed
        bookedSlot = passedData["bookedSlot"]
        date = passedData["date"]
        hospitalId = passedData["hospitalId"]
        requiredCount = passedData["requiredCount"]
        try:
            result = AppointmentsDB.objects.filter(
                dateString=date,
                timeString=bookedSlot,
                hospitalID=hospitalId,
            )
            # return true if appointment can be added
            return Response({
                    "count": (result.count() <= requiredCount)
                }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Appointment Check: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)


class AppointmentSpecificView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        now = timezone.now()
        criterion1 = Q(patientID__exact=self.kwargs['user_id'])
        criterion2 = Q(timestamp__gte=now)
        return AppointmentsDB.objects.filter(
            criterion1 & criterion2
            ).order_by('timestamp')


class AppointmentDoctorSpecific(ListAPIView):
    """Get a doctors specific appointments"""
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        now = timezone.now()
        criterion1 = Q(doctorID__exact=self.kwargs['doctorID'])
        criterion2 = Q(timestamp__gte=now)
        return AppointmentsDB.objects.filter(
            criterion1 & criterion2
            ).order_by('timestamp')


class AppointmentGeneralView(ListAPIView):
    """Get all users appointments"""
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        now = timezone.now()
        return AppointmentsDB.objects.filter(
            timestamp__gte=now).order_by('timestamp')
