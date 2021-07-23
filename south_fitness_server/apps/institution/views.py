import uuid

import bugsnag
from rest_framework import views,  status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Institutions
from .serializers import InstitutionSerializer


class Institution(views.APIView):
    """
        Add notifications details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add appointment to DB """
        try:
            # Save data to DB
            serializer = InstitutionSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(institute_id=uuid.uuid1())
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
        """ Add appointment to DB """
        institute = Institutions.objects.get(institute_id=request.data["institute_id"])
        try:
            # Save data to DB
            serializer = InstitutionSerializer(institute, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
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


class AllInstitutions(generics.ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = InstitutionSerializer

    def get_queryset(self):
        return Institutions.objects.filter().order_by('createdAt')
