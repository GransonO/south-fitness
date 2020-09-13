# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .models import StaffDB
from .serializers import StaffSerializer
from datetime import datetime
import requests


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
            StaffDB.objects.filter(
                staffID=passedData["staffID"]).update(
                        hospitalID=passedData["hospitalID"],
                        staffID=passedData["staffID"],
                        staffEmail=passedData["staffEmail"],
                        staffName=passedData["staffName"],
                        staffImage=passedData["staffImage"],
                        staffDepartment=passedData["staffDepartment"],
                        staffPhone=passedData["staffPhone"],
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
            onlineStatus = doctorState.onlineStatus
            currentState = True
            doctorToken = doctorState.staffToken
            doctorName = doctorState.staffToken
            message = "Hello {}, you have an online video call. The patient is ready".format(doctorState.staffName)
            if(currentlyOnCall & onlineStatus):
                currentState = False
                message = "Hello {}, you have an online video call. The patient is ready. Please login to your RFH doctor's app".format(doctorState.staffName)

            notifyDoctor(doctorToken, message)

            return Response({
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

        myHeaders={
            "Authorization": "key=AAAAxTAONtw:APA91bHOkfYKzBkGvUj4NMzK8JTaWHDwf8g_GAxDeMPvijZ2IdWu3C1mjdsIRSKl1c8oBaGP4C7YSrSsJ-H09zofTepJEREMu7-8KTV5oSK9lqlBoCtyNb8wDJIHBG7IHkQXC4V3dbRU",
            "content-type": "application/json"
            }

        messageBody={
            "title": "RFH Online consultation reminder",
            "text": message
        }

        myData = { 
            "registration_ids": [doctorToken],
            "notification" : messageBody,
            "data": {
                "page": "NOTIFICATION"
            }
        }

        requests.post(url, headers=myHeaders, data=myData)


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
