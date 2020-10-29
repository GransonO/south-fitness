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
from ..accounts.models import Accounts, DoctorAccount
from ..accounts.serializers import AccountSerializer, DoctorAccountSerializer
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
                amountPayed=passedData["amountPayed"],
                mpesaPaymentId=passedData["mpesaPaymentId"],
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
                    sosStatus=True,
                    docComplete=False
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
            sosResult = SOSAppointments.objects.get(
                sosID=passedData["sosID"])
            count = sosResult.trialCount + 1
            passedData["trialCount"] = count
            serializer = SOSSerializer(
                sosResult, data=passedData, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            result = FcmDB.objects.get(user_id=passedData["patientID"])
            if(passedData["iscomplete"]):
                # Update account state
                if(passedData["sosID"] != "null"):
                    # is SOS
                    EmergencyStateView.accounts(passedData, True, result.token)
                else:
                    # is not SOS
                    EmergencyStateView.accounts(passedData, False, result.token)
            else:
                if(passedData["docComplete"]):
                    EmergencyStateView.notifyPatient(
                        result.token,
                        passedData["doctorID"],
                        passedData["sosID"],
                        "Emergency session complete",
                        "The doctor completed your session. Kindly confirm if the session was successful",
                        "NOTIFICATION")
                else:
                    EmergencyStateView.notifyPatient(
                        result.token,
                        passedData["doctorID"],
                        passedData["sosID"],
                        "Emergency doctor found",
                        "We've found a doctor to assist you.",
                        "SOS")

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

    def notifyPatient(patientToken, docId, sosID, title, body, page):
        """Send notification to the doctor"""
        url = 'https://fcm.googleapis.com/fcm/send'

        myHeaders = {
            "Authorization": "key=AAAAFXoiEbA:APA91bGIVyHsWKPt31ZoeCbi7zSqYIXyZQ3eS7Tq0aMpFT58BVWGe6KhlF_rpCIecZJGAKOotIRkhvDtlTHoXF1lyo7XAdsCxGn3pG5wYnvcTusMJHwiAnAWy1-sBaO89QFJs59DlBhL",
            "content-type": "application/json"
            }

        myData = {
            "registration_ids": [patientToken],
            "notification": {
                "title": title,
                "text": body,
            },
            "data": {
                "sosStatus": "accepted",
                "page": page,
                "sosID": sosID,
                "docId": docId,
                "title" : title,
                "body" : body,
            }
        }

        background = {
            "registration_ids": [patientToken],
            "data": {
                "sosStatus": "accepted",
                "page": page,
                "sosID": sosID,
                "docId": docId,
                "title" : title,
                "body" : body,
            }
        }

        y = requests.post(url, headers=myHeaders, data=json.dumps(background))
        x = requests.post(url, headers=myHeaders, data=json.dumps(myData))
        print("message sent : {}".format(y))
        print("message sent : {}".format(x))

    def accounts(passedData, status, token):
        if(status):
            # is SOS
            # Appointment
            appResult = AppointmentsDB.objects.get(
                appointmentID=passedData["sosID"])
            # SOS
            sosResult = SOSAppointments.objects.get(
                sosID=passedData["sosID"])
            #  Update accounts
            account_data = Accounts(
                doctorID=sosResult.doctorID,
                appointmentID=sosResult.sosID,
                patientID=sosResult.patientID,
                amountPaid=appResult.amountPayed,
                doctorsAmount=(appResult.amountPayed * 0.7),
                paymentId=appResult.mpesaPaymentId)
            account_data.save()
            # Update Doctors data
            doctorResult = DoctorAccount.objects.filter(
                doctorID=sosResult.doctorID)
            if(len(doctorResult) < 1):
                # create new
                docData = DoctorAccount(
                    doctorID=sosResult.doctorID,
                    callCount=1,
                    earnedTotal=(appResult.amountPayed * 0.7),
                    currentAmount=(appResult.amountPayed * 0.7)
                )
                docData.save()
            else:
                theDoctor = doctorResult[0]
                doctorResult.update(
                    callCount=theDoctor.callCount + 1,
                    earnedTotal=theDoctor.earnedTotal + (appResult.amountPayed * 0.7),
                    currentAmount=theDoctor.currentAmount + (appResult.amountPayed * 0.7)
                )
        else:
             # is NOT SOS
            # Appointment
            appResult = AppointmentsDB.objects.get(
                appointmentID=passedData["appointmentId"])

            #  Update accounts
            account_data = Accounts(
                doctorID=appResult.doctorID,
                appointmentID=appResult.appointmentID,
                patientID=appResult.patientID,
                amountPaid=appResult.amountPayed,
                doctorsAmount=(appResult.amountPayed * 0.7),
                paymentId=appResult.mpesaPaymentId)
            account_data.save()
            # Update Doctors data
            doctorResult = DoctorAccount.objects.filter(
                doctorID=appResult.doctorID)
            if(len(doctorResult) < 1):
                # create new
                docData = DoctorAccount(
                    doctorID=appResult.doctorID,
                    callCount=1,
                    earnedTotal=(appResult.amountPayed * 0.7),
                    currentAmount=(appResult.amountPayed * 0.7)
                )
                docData.save()
            else:
                theDoctor = doctorResult[0]
                print("doctorResult - - - - - -> {}".format(theDoctor))
                doctorResult.update(
                    callCount=theDoctor.callCount + 1,
                    earnedTotal=theDoctor.earnedTotal + (appResult.amountPayed * 0.7),
                    currentAmount=theDoctor.currentAmount + (appResult.amountPayed * 0.7)
                )

        EmergencyStateView.notifyPatient(
            result.token,
            "",
            "",
            "Session complete",
            "Your session has been completed",
            "NOTIFICATION")

class userEmergencies(ListAPIView):
    """Get all users appointments"""
    serializer_class = SOSSerializer

    def get_queryset(self):
        now = timezone.now()
        criterion1 = Q(patientID__exact=self.kwargs['user_id'])
        criterion2 = Q(iscomplete__exact=False)
        return SOSAppointments.objects.filter(
            criterion1 & criterion2).order_by('timestamp')