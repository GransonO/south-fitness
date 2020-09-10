from django.db import models
from datetime import datetime


class FcmDB(models.Model):
    """Profiles ref Number"""
    token = models.CharField(
        unique=True, max_length=1050, default='non')
    user_id = models.CharField(max_length=250, default='non')
    platform = models.CharField(max_length=250, default='non')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'platform : {} ,user_id: {}'.format(
            self.platform, self.user_id)
