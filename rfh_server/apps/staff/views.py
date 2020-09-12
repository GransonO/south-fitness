# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .models import StaffDB
from .serializers import StaffSerializer
from datetime import datetime


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
    def put(request):
        passedData = request.data
        try:
            StaffDB.objects.filter(
                staffID=passedData["staffID"]).update(
                        onlineStatus=passedData["onlineStatus"],
                        currentlyOnCall=passedData["currentlyOnCall"],
                        # lastLoggedIn=datetime.now,
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
