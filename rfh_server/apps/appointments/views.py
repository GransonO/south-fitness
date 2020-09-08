# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import AppointmentsDB


class AppointmentsViews(views.APIView):
    """
        Pick all MPESA details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Reassign Tier groups to members """
        passedData = request.data
        print("The passedData is -------------: {}".format(passedData))

        body = passedData['Body']
        callback_body = body['stkCallback']
        MerchantRequestID = callback_body['MerchantRequestID']
        ResultCode = callback_body['ResultCode']
        ResultDesc = callback_body['ResultDesc']
        CallbackMetadata = callback_body['CallbackMetadata']

        Item = CallbackMetadata['Item']
        if(len(Item) < 5):
            Amount = Item[0]['Value']
            MpesaReceiptNumber = Item[1]['Value']
            TransactionDate = Item[2]['Value']
            PhoneNumber = Item[3]['Value']
        else:
            Amount = Item[0]['Value']
            MpesaReceiptNumber = Item[1]['Value']
            TransactionDate = Item[3]['Value']
            PhoneNumber = Item[4]['Value']

        # Save data to DB
        mpesa_data = AppointmentsDB(
            MerchantRequestID=MerchantRequestID,
            ResultCode=ResultCode,
            ResultDesc=ResultDesc,
            Amount=Amount,
            MpesaReceiptNumber=MpesaReceiptNumber,
            TransactionDate=TransactionDate,
            Client_phone=PhoneNumber
        )
        mpesa_data.save()
        return Response({"DONE"}, status.HTTP_200_OK)

    @staticmethod
    def put(request):
        """Get the Mpesa value deposited"""
        passedData = request.data
        trans_num = passedData["MerchantRequestID"]
        try:
            result = AppointmentsDB.objects.get(
                MerchantRequestID=trans_num)
            print("The responce is : {}".format(result))
            return Response({
                    "status": "success",
                    "code": 1,
                    "customer_phone": result.Client_phone,
                    "receipt_number": result.MpesaReceiptNumber,
                    "amount": result.Amount,
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
                    "count": (result.count() < requiredCount)
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
    def put(request):
        """Get the Mpesa value deposited"""
        passedData = request.data
        trans_num = passedData["MerchantRequestID"]
        try:
            result = AppointmentsDB.objects.get(
                MerchantRequestID=trans_num)
            print("The responce is : {}".format(result))
            return Response({
                    "status": "success",
                    "code": 1,
                    "customer_phone": result.Client_phone,
                    "receipt_number": result.MpesaReceiptNumber,
                    "amount": result.Amount,
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
