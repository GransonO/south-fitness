from django.db import models
from datetime import datetime

class Accounts(models.Model):

    appointmentId = models.CharField(unique=True, max_length=250, default='non')
    patientID = models.CharField(max_length=250, default='non')
    doctorID = models.CharField(max_length=250, default='non')
    amountPaid = models.IntegerField(default=0)
    doctorsAmount = models.FloatField(default=0.0)
    paymentId = models.CharField(unique=True, max_length=250, default='non')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'appointmentId : {} ,amountPaid: {}'.format(
            self.appointmentId, self.amountPaid)

class DoctorAccount(models.Model):

    doctorID = models.CharField(unique=True, max_length=250, default='non')
    callCount = models.IntegerField(default=0)
    earnedTotal = models.FloatField(default=0.0)
    amountWithdrawn = models.FloatField(default=0.0)
    currentAmount = models.FloatField(default=0.0)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'doctorID : {} ,currentAmount: {}'.format(
            self.doctorID, self.currentAmount)

class WithdrawalAccount(models.Model):

    withdrawID = models.CharField(unique=True, max_length=250, default='non')
    doctorID = models.CharField(max_length=250, default='non')
    amountWithdrawn = models.FloatField(default=0.0)
    currentAmount = models.CharField(max_length=250, default='non')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'withdrawID : {} ,amountWithdrawn: {}'.format(
            self.withdrawID, self.amountWithdrawn)