# Create your views here.
import bugsnag
from django.contrib.auth.models import User
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView


class Authenticate(views.APIView):
    """
        Deal with Authentication
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add FCM No to DB """
        passedData = request.data
        try:
            # Check if it exists
            user = User.objects.create_user(
                passedData["firstname"],
                passedData["email"],
                passedData["password"]
                )
                return Response({
                    "status": "success",
                    "code": 1
                    }, status.HTTP_200_OK)
            else:
                # Add user to Users DB

                return Response({
                        "status": "success",
                        "code": 1
                        }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('ProfilesRef Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)
