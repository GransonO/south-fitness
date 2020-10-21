# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import AppointmentsDB, SOSAppointments
from rest_framework.generics import ListAPIView
from .serializers import AppointmentSerializer, SOSSerializer
from django.db.models import Q
from django.utils import timezone
from ..staff.models import StaffDB
from ..fcm.models import FcmDB
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

            apType = "General"
            if(passedData["type"] == 2):
                apType = "Online"

            if(passedData["type"] == 0):
                apType = "Emergency"

            message = "A new {} appointment has been posted".format(apType)

            if(passedData["type"] == 0):
                # Immediate request
                # Save SOS data
                sos_data = SOSAppointments(
                    sosID=passedData["id"],
                    patientID=passedData["patient_id"],
                    summary=passedData["summary"],
                    sosStatus=True
                )
                sos_data.save()
                # 1. Check for all online doctors
                criterion1 = Q(onlineStatus__exact=True)
                criterion2 = Q(staffDepartment="1001")
                staffData = StaffDB.objects.filter(
                    criterion1 & criterion2
                )
                allTokens = []
                for x in staffData:
                    allTokens.append(x.staffToken)
                # 2. Send FCM to all
                AppointmentsViews.notifyOnlineStaff(allTokens, message, passedData) 

                # 3. Receive post request from first acceptor
                # 4. If none accepts, resend after 2 mins


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

    def notifyOnlineStaff(allTokens, message, passedData):
        """Send notification to the doctor"""
        url = 'https://fcm.googleapis.com/fcm/send'

        myHeaders = {
            "Authorization": "key=AAAAFXoiEbA:APA91bGIVyHsWKPt31ZoeCbi7zSqYIXyZQ3eS7Tq0aMpFT58BVWGe6KhlF_rpCIecZJGAKOotIRkhvDtlTHoXF1lyo7XAdsCxGn3pG5wYnvcTusMJHwiAnAWy1-sBaO89QFJs59DlBhL",
            "content-type": "application/json"
            }

        messageBody = {
            "title": "Emergency alert",
            "text": message,
            "icon": "https://res.cloudinary.com/dolwj4vkq/image/upload/v1578849920/RFH/RFH-colored-white-icon.png",
        }

        myData = {
            "registration_ids": allTokens,
            "notification": messageBody,
            "data": {
                "patientId": passedData["patient_id"],
                "sosID": passedData["id"],
                "page": "SOS",
                "title" : "Emergency Alert",
                "body" : "Click to start the call",
            }
        }

        background = {
            "registration_ids": allTokens,
            "data": {
                "patientId": passedData["patient_id"],
                "sosID": passedData["id"],
                "page": "SOS",
                "title" : "Emergency Alert",
                "body" : "Click to start the call",
            }
        }

        y = requests.post(url, headers=myHeaders, data=json.dumps(background))
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
        criterion3 = Q(appointmentType__gt=0)
        return AppointmentsDB.objects.filter(
            criterion1 & criterion2 & criterion3
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

class EmergencyView(ListAPIView):
    """Get all users appointments"""
    serializer_class = SOSSerializer

    def get_queryset(self):
        now = timezone.now()
        return SOSAppointments.objects.filter(
            sosStatus__exact=True).order_by('timestamp')

class EmergencyStateView(views.APIView):
    """Get all users appointments"""
    serializer_class = SOSSerializer
    @staticmethod
    def put(request):
        passedData = request.data
        try:
            result = SOSAppointments.objects.get(
                sosID=passedData["sosID"])
            count = result.trialCount + 1
            passedData["trialCount"] = count
            print("--------------------***-------------------- {}".format(passedData))
            serializer = SOSSerializer(
                result, data=passedData, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            if(passedData["iscomplete"]):
                pass
            else:
                result = FcmDB.objects.get(user_id=passedData["patientID"])
                EmergencyStateView.notifyPatient(result.token, passedData["doctorID"])
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

    def notifyPatient(patientToken, docId):
        """Send notification to the doctor"""
        url = 'https://fcm.googleapis.com/fcm/send'

        myHeaders = {
            "Authorization": "key=AAAAFXoiEbA:APA91bGIVyHsWKPt31ZoeCbi7zSqYIXyZQ3eS7Tq0aMpFT58BVWGe6KhlF_rpCIecZJGAKOotIRkhvDtlTHoXF1lyo7XAdsCxGn3pG5wYnvcTusMJHwiAnAWy1-sBaO89QFJs59DlBhL",
            "content-type": "application/json"
            }

        myData = {
            "registration_ids": [patientToken],
            "notification": {
                "title": "Emergency doctor found",
                "text": "We've found a doctor to assist you.",
            },
            "data": {
                "sosStatus": "accepted",
                "page": "SOS",
                "docId": docId,
                "title" : "Emergency doctor found",
                "body" : "We've found a doctor to assist you.",
            }
        }

        background = {
            "registration_ids": [patientToken],
            "data": {
                "sosStatus": "accepted",
                "page": "SOS",
                "docId": docId,
                "title" : "Emergency doctor found",
                "body" : "We've found a doctor to assist you.",
            }
        }

        y = requests.post(url, headers=myHeaders, data=json.dumps(background))
        x = requests.post(url, headers=myHeaders, data=json.dumps(myData))
        print("message sent : {}".format(y))
        print("message sent : {}".format(x))

class userEmergencies(ListAPIView):
    """Get all users appointments"""
    serializer_class = SOSSerializer

    def get_queryset(self):
        now = timezone.now()
        criterion1 = Q(patientID__exact=self.kwargs['user_id'])
        criterion2 = Q(iscomplete__exact=False)
        return SOSAppointments.objects.filter(
            criterion1 & criterion2).order_by('timestamp')