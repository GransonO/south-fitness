from rest_framework import views, status
from .serializers import (AccountSerializer, DoctorAccountSerializer, WithdrawalAccountSerializer)
from .models import (Accounts, DoctorAccount, WithdrawalAccount)
from rest_framework.response import Response


class Accounts(views.APIView):
    """ Accounts  """

    @staticmethod
    def get(request):
        passed_data = request.data
        print("The passedData is ----------------------------: {}".format(passed_data))
        return Response({"The server is woke as needed"}, status.HTTP_200_OK)

    @staticmethod
    def post(request):
        passed_data = request.data
        print("The passedData is ----------------------------: {}".format(passed_data))
        return Response({"The server is woke as needed"}, status.HTTP_200_OK)
