from django.db import models
from datetime import datetime


class StaffDB(models.Model):
    """Staff DB"""
    enabled = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
    hospitalID = models.CharField(max_length=250, default='non', null=True)

    staffID = models.CharField(unique=True, max_length=250, default='non')
    staffEmail = models.CharField(unique=True, max_length=250, default='non')
    staffName = models.CharField(max_length=250, default='non')
    staffGender = models.CharField(max_length=250, default='Male')
    staffImage = models.CharField(max_length=250, default='non')
    staffDepartment = models.CharField(max_length=250, default='non')
    staffPhone = models.CharField(unique=True, max_length=250, default='non')

    # if logged in doctors phone
    onlineStatus = models.BooleanField(default=False)
    lastLoggedIn = models.DateTimeField(default=datetime.now)
    # if oncall with a patient
    currentlyOnCall = models.BooleanField(default=False)
    staffToken = models.CharField(max_length=550, default='non')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'staffEmail : {} ,staffID: {}'.format(
            self.staffEmail, self.staffID)
