from django.db import models
from datetime import datetime


class ProfilesDB(models.Model):
    """Profiles DB"""
    fullname = models.CharField(max_length=250, default='non')
    email = models.CharField(unique=True, max_length=250, default='non')
    birthDate = models.DateTimeField(default=datetime.now)
    activation_code = models.CharField(max_length=250, default='non')
    user_id = models.CharField(max_length=350, default='non')
    team = models.CharField(max_length=250, default='non')

    gender = models.CharField(max_length=250, default='non')
    image = models.CharField(
        max_length=1250,
        default="https://res.cloudinary.com/dolwj4vkq/image/upload/v1621266421/South_Fitness/profile_images/avatar.jpg"
    )
    height = models.FloatField(default=0.0)
    weight = models.FloatField(default=0.0)

    goal = models.CharField(max_length=550, default='non')
    discipline = models.CharField(max_length=550, default='non')
    workout_duration = models.CharField(max_length=550, default='non')
    user_type = models.CharField(max_length=100, default='USER')
    institution = models.CharField(max_length=100, default='EPITOME')
    is_active = models.BooleanField(default=True)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'email : {} ,fullname: {}'.format(
            self.email, self.fullname)
