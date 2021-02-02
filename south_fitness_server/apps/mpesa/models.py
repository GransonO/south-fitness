from django.db import models
from datetime import datetime


class MpesaEntryModel(models.Model):
    MerchantRequestID = models.CharField(
        unique=True, max_length=250, default='non')


class MpesaEntryDB(models.Model):

    MerchantRequestID = models.CharField(
        unique=True, max_length=250, default='non')
    ResultCode = models.IntegerField(default='1')
    ResultDesc = models.CharField(max_length=250, default='non')
    Amount = models.FloatField(default=0.0)
    MpesaReceiptNumber = models.CharField(
        unique=True, max_length=250, default='non')
    TransactionDate = models.CharField(max_length=250, default='non')
    Client_phone = models.CharField(max_length=250, default='non')
    request_date = models.DateTimeField(default=datetime.now)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'id : {} ,phone: {}'.format(
            self.MerchantRequestID, self.Client_phone)
