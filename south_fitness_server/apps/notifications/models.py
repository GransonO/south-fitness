from django.db import models
from datetime import datetime


class NotificationsDB(models.Model):

    notification_id = models.CharField(
        unique=True, max_length=250, default='non')
    user_id = models.CharField(max_length=250, default='non')
    title = models.CharField(max_length=250, default='non')
    details = models.CharField(max_length=550, default='non')
    viewed = models.IntegerField(default=0)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'title : {} ,user_id: {}'.format(
            self.title, self.user_id)
