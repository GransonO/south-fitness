from django.db import models
from datetime import datetime


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


class ProfilesDB(models.Model):
    """Profiles DB"""
    UserRefId = models.CharField(
        unique=True, max_length=250, default='non')
    birthDate = models.DateTimeField(default=datetime.now)
    chattingWith = models.CharField(max_length=250, default='non', null=True)
    doc = models.BooleanField(default=False)
    email = models.CharField(unique=True, max_length=250, default='non')
    firstname = models.CharField(max_length=250, default='non')
    lastname = models.CharField(max_length=250, default='non')
    gender = models.CharField(max_length=250, default='non')
    userId = models.CharField(unique=True, max_length=250, default='non')
    nickname = models.CharField(max_length=250, default='non')
    phone = models.CharField(max_length=250, default='non')
    photoUrl = models.CharField(max_length=550, default='non')

    # Insurance $ relatives
    relatives = models.CharField(max_length=550, default='non')
    insurance = models.CharField(max_length=550, default='non')

    # Location details
    address = models.CharField(max_length=250, default='non')
    addressId = models.CharField(max_length=250, default='non')
    addressName = models.CharField(max_length=250, default='non')
    latitude = models.FloatField(max_length=250, default=0.0)
    longitude = models.FloatField(max_length=250, default=0.0)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'email : {} ,firstname: {}'.format(
            self.email, self.firstname)
