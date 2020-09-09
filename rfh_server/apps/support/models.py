from django.db import models
from datetime import datetime


class SupportDB(models.Model):

    support_id = models.CharField(
        unique=True, max_length=250, default='non')
    user_id = models.CharField(max_length=250, default='non')
    title = models.CharField(max_length=250, default='non')
    details = models.CharField(max_length=1050, default='non')
    image = models.CharField(max_length=250, default='non')
    response = models.CharField(max_length=1050, default='non')
    tracker = models.BooleanField(default=False)
    dateTime = models.DateTimeField(default=datetime.now)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'title : {} ,user_id: {}'.format(
            self.title, self.support_id)
