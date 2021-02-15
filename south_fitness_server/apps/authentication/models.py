from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Reset(models.Model):
    """Profiles ref Number"""
    reset_code = models.CharField(max_length=4)
    user_email = models.CharField(unique=True, max_length=250, default='non')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'platform : {} ,user_id: {}'.format(
            self.reset_code, self.user_email)


class Activation(models.Model):
    """Profiles ref Number"""
    activation_code = models.IntegerField()
    user_email = models.CharField(unique=True, max_length=250, default='non')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'platform : {} ,user_id: {}'.format(
            self.activation_code, self.user_email)
