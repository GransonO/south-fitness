# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from django.db.models import Q
from .models import TeamsDB
from .serializers import TeamsSerializer
import requests
import json


class Teams(views.APIView):
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
            support_data = TeamsDB(
                teams_id=passedData["teams_id"],
                team_name=passedData["team_name"],
                slogan=passedData["slogan"],
                image=passedData["image"],
                created_by=passedData["created_by"],
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
            TeamsDB.objects.filter(
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


class Test(views.APIView):

    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        nums = [1, 2, 147, 483, 647]
        for num in nums:
            x = int("{0:b}".format(num))
            print("*********{}".format(x))
            a = Test.solution(x)
            print("-------------------{}".format(a))
        return Response({"THIS HAS BEEN RETURNED"}, status.HTTP_200_OK)

    @staticmethod
    def solution(n):
        # write your code in Python 3.6
        x = (str(n).split("01"))
        print("-----***-----{}".format(x))
        if max(x) is '' or '10':
            return 0
        return len(max(x))


class TeamsAllView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = TeamsSerializer

    def get_queryset(self):
        return TeamsDB.objects.filter().order_by('dateTime')


class TeamsSpecificView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = TeamsSerializer

    def get_queryset(self):
        return TeamsDB.objects.filter(
            notification_id=self.kwargs['support_id']
            ).order_by('dateTime')


class TeamsUserView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = TeamsSerializer

    def get_queryset(self):
        criterion = Q(user_id__contains=self.kwargs['user_id'])
        return TeamsDB.objects.filter(criterion).order_by('dateTime')
