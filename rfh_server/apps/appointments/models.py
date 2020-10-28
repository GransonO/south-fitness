from django.db import models
from datetime import datetime


class AppointmentsDB(models.Model):

    doctorID = models.CharField(max_length=250, default='non')
    doctorName = models.CharField(max_length=250, default='non')
    stateColor = models.CharField(max_length=250, default='non')
    status = models.CharField(max_length=250, default='non')
    dateString = models.CharField(max_length=250, default='non')
    timeString = models.CharField(max_length=250, default='non')
    hospitalID = models.CharField(max_length=250, default='non')
    hospitalPhone = models.CharField(max_length=250, default='non')
    hospitalName = models.CharField(max_length=250, default='non')
    appointmentID = models.CharField(unique=True, max_length=250, default='non')
    patientID = models.CharField(max_length=250, default='non')
    paymentType = models.CharField(max_length=250, default='non')
    patientPhone = models.CharField(max_length=250, default='non')
    appointmentState = models.CharField(max_length=250, default='non')
    summary = models.CharField(max_length=550, default='non')
    mpesaPaymentId = models.CharField(max_length=550, default='non')
    amountPayed = models.FloatField(default=0.0)
    appointmentType = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=datetime.now)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'id : {} ,phone: {}'.format(
            self.patientID, self.patientPhone)

class SOSAppointments(models.Model):

    sosID = models.CharField(unique=True, max_length=250, default='non')
    summary = models.CharField(max_length=550, default='non')
    patientID = models.CharField(max_length=250, default='non')
    doctorID = models.CharField(max_length=250, default='non')
    sosStatus = models.BooleanField(default=True)
    trialCount = models.IntegerField(default='0')
    timestamp = models.DateTimeField(default=datetime.now)
    iscomplete = models.BooleanField(default=True)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'id : {} ,phone: {}'.format(
            self.patientID, self.sosStatus)
