from rest_framework.serializers import ModelSerializer
from .models import AppointmentsDB, SOSAppointments


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


class SOSSerializer(ModelSerializer):

    class Meta:
        model = SOSAppointments
        fields = [
            "sosID",
            "summary",
            "patientID",
            "doctorID",
            "sosStatus",
            "trialCount",
            "timestamp",
            "createdAt"
        ]
