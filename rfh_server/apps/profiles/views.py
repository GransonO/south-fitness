# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .models import ProfilesRefDB, ProfilesDB
from .serializers import ProfileSerializer


class Profiles(views.APIView):
    """
        Add Profiles details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add Profiles to DB """
        passedData = request.data
        try:
            # Save data to DB
            profile_data = ProfilesDB(
                    UserRefId=passedData["UserRefId"],
                    birthDate=passedData["birthDate"],
                    chattingWith=passedData["chattingWith"],
                    doc=passedData["doc"],
                    email=passedData["email"],
                    firstname=passedData["firstname"],
                    lastname=passedData["lastname"],
                    gender=passedData["gender"],
                    userId=passedData["userId"],
                    nickname=passedData["nickname"],
                    phone=passedData["phone"],
                    photoUrl=passedData["photoUrl"],
                    relatives=passedData["relatives"],
                    insurance=passedData["insurance"],
                    address=passedData["address"],
                    addressId=passedData["addressId"],
                    addressName=passedData["addressName"],
                    latitude=passedData["latitude"],
                    longitude=passedData["longitude"],
            )
            profile_data.save()
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
    def put(request):
        passedData = request.data
        # Check This later
        try:
            ProfilesDB.objects.filter(
                userId=passedData["userId"]).update(
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


class ProfilesAllView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return ProfilesDB.objects.filter().order_by('createdAt')


class ProfileSpecificView(ListAPIView):
    """Get a user specific appointments"""
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return ProfilesDB.objects.filter(
            userId=self.kwargs['userId']
            ).order_by('createdAt')


class ProfileRef(views.APIView):
    """
        Deal with Prefs
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add REF No to DB """
        passedData = request.data
        try:
            result = ProfilesRefDB.objects.filter(user_id=passedData["user_id"])
            if(result.count() < 1):
                # Save data to DB
                ProfilesRef_data = ProfilesRefDB(
                    refNum=passedData["refNum"],
                    user_id=passedData["user_id"],
                    hospital=passedData["hospital"]
                )
                ProfilesRef_data.save()
                return Response({
                    "message": "User REF added"
                    "status": "success",
                    "code": 1
                    }, status.HTTP_200_OK)
            else:
                return Response({
                    "message": "User REF exists"
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

    @staticmethod
    def put(request):
        passedData = request.data
        try:
            result = ProfilesRefDB.objects.filter(refNum=passedData["refNum"])
            return Response({
                    "status": "success",
                    "exists": (0 < result.count()),
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
