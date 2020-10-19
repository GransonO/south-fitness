# Create your views here.
import bugsnag
import requests
import json
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q
from .models import StaffDB
from .serializers import StaffSerializer


class Staff(views.APIView):
    """
        Add Staff details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add Profiles to DB """
        passedData = request.data
        try:
            # Save data to DB
            staff_data = StaffDB(
                    hospitalID=passedData["hospitalID"],
                    staffID=passedData["staffID"],
                    staffEmail=passedData["staffEmail"],
                    staffName=passedData["staffName"],
                    staffImage=passedData["staffImage"],
                    staffDepartment=passedData["staffDepartment"],
                    staffPhone=passedData["staffPhone"],
                    staffGender=passedData["staffGender"]
                )
            staff_data.save()
            return Response({
                "status": "success",
                "code": 1
                }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('staff Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)

    @staticmethod
    def put(request):
        passedData = request.data
        try:
            staff = StaffDB.objects.get(staffID=passedData["staffID"])
            serializer = StaffSerializer(
                staff, data=passedData, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            if(passedData["notify"] == True):
                Staff.email(staff.staffName, staff.staffEmail)

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
    def email(name, email):
        print("------ name: {}. Email:{}".format(name, email))
        subject = 'Welcome to RFH Online Doctor'
        html_message = render_to_string("email.html", {'context': 'values'})
        plain_message = strip_tags(html_message)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)


class StaffState(views.APIView):
    """
        Add Staff details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        passedData = request.data
        try:
            doctorState = StaffDB.objects.get(
                staffID=passedData["staffID"]
                )
            currentlyOnCall = doctorState.currentlyOnCall
            currentState = doctorState.onlineStatus
            doctorToken = doctorState.staffToken
            message = "Hello {}, you have an online video call. The patient is ready".format(doctorState.staffName)
            if(currentlyOnCall):
                currentState = False
                message = "Hello {}, you have an online video call. The patient is ready. Please login to your RFH doctor's app".format(doctorState.staffName)

            StaffState.notifyDoctor(doctorToken, message)

            return Response({
                    "doctorToken": doctorToken,
                    "available": currentState,
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

    def notifyDoctor(doctorToken, message):
        """Send notification to the doctor"""
        url = 'https://fcm.googleapis.com/fcm/send'

        myHeaders = {
            "Authorization": "key=AAAAxTAONtw:APA91bHOkfYKzBkGvUj4NMzK8JTaWHDwf8g_GAxDeMPvijZ2IdWu3C1mjdsIRSKl1c8oBaGP4C7YSrSsJ-H09zofTepJEREMu7-8KTV5oSK9lqlBoCtyNb8wDJIHBG7IHkQXC4V3dbRU",
            "content-type": "application/json"
            }

        messageBody = {
            "title": "RFH Online consultation reminder",
            "text": message
        }

        myData = {
            "registration_ids": [doctorToken],
            "notification": messageBody,
            "data": {
                "page": "NOTIFICATION"
            }
        }

        x = requests.post(url, headers=myHeaders, data=json.dumps(myData))
        print("message sent : {}".format(x))

    @staticmethod
    def put(request):
        passedData = request.data
        try:
            StaffDB.objects.filter(
                staffID=passedData["staffID"]).update(
                        onlineStatus=passedData["onlineStatus"],
                        currentlyOnCall=passedData["currentlyOnCall"],
                        staffToken=passedData["staffToken"],
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


class StaffAllView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = StaffSerializer

    def get_queryset(self):
        return StaffDB.objects.filter().order_by('createdAt')


class StaffSpecificView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = StaffSerializer

    def get_queryset(self):
        return StaffDB.objects.filter(
            staffID=self.kwargs['staffID']
            ).order_by('createdAt')


class StaffDoctorsView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = StaffSerializer

    def get_queryset(self):
        return StaffDB.objects.filter(
            staffDepartment='1001'
            ).order_by('createdAt')


class StaffSpecificEmail(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = StaffSerializer

    def get_queryset(self):
        return StaffDB.objects.filter(
            staffEmail=self.kwargs['staff_email']
            ).order_by('createdAt')


class AllAvailableDocs(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = StaffSerializer

    def get_queryset(self):
        now = timezone.now()
        criterion1 = Q(onlineStatus=True)
        criterion2 = Q(currentlyOnCall=False)
        criterion3 = Q(enabled=True)
        return StaffDB.objects.filter(
            criterion1 & criterion2 & criterion3
            )
