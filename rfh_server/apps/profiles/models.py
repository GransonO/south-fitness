from django.db import models


class ProfilesRefDB(models.Model):
    """pROFILES ref Number"""
    refNum = models.CharField(
        unique=True, max_length=250, default='non')
    user_id = models.CharField(max_length=250, default='non')
    hospital = models.CharField(max_length=250, default='non')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'hospital : {} ,user_id: {}'.format(
            self.hospital, self.user_id)
