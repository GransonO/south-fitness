from rest_framework.serializers import ModelSerializer
from .models import (Accounts, DoctorAccount, WithdrawalAccount)


class AccountSerializer(ModelSerializer):

    class Meta:
        model = Accounts
        fields = [
            "appointmentID",
            "patientID",
            "doctorID",
            "amountPaid",
            "callCount",
            "doctorsAmount",
            "paymentId",
            "createdAt",
            "updatedAt"
        ]

class DoctorAccountSerializer(ModelSerializer):

    class Meta:
        model = DoctorAccount
        fields = [
            "doctorID",
            "earnedTotal",
            "amountWithdrawn",
            "currentAmount",
            "createdAt",
            "updatedAt"
        ]

class WithdrawalAccountSerializer(ModelSerializer):

    class Meta:
        model = WithdrawalAccount
        fields = [
            "withdrawID",
            "doctorID",
            "amountWithdrawn",
            "currentAmount",
            "createdAt",
            "updatedAt"
        ]