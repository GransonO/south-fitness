from rest_framework.serializers import ModelSerializer
from .models import AppointmentsDB


class AppointmentSerializer(ModelSerializer):

    class Meta:
        model = AppointmentsDB
        fields = [
            "doctorID",
            "doctorName",
            "stateColor",
            "status",
            "dateString",
            "timeString",
            "hospitalID",
            "hospitalPhone",
            "hospitalName",
            "appointmentID",
            "patientID",
            "paymentType",
            "patientPhone",
            "appointmentState",
            "summary",
            "appointmentType",
            "timestamp",
            "createdAt"
        ]
