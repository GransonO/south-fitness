# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from django.db.models import Q
from .models import TeamsDB
from .serializers import TeamsSerializer


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
