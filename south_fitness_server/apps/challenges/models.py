from django.db import models


class MvtChallenge(models.Model):
    """ Run Challenge """
    challengeId = models.CharField(max_length=250, default='non')
    challengeType = models.CharField(max_length=250, default='non')
    team = models.CharField(max_length=250, default='non')

    user_id = models.CharField(max_length=250, default='non')

    distance = models.FloatField(default=0.0)  # in metres
    steps_count = models.IntegerField(default=0)
    caloriesBurnt = models.FloatField(default=0.0)  # kcl
    startTime = models.DateTimeField(auto_now_add=True, null=True)
    endTime = models.DateTimeField(auto_now=True, null=True)

    start_latitude = models.FloatField(default=0.0)
    start_longitude = models.FloatField(default=0.0)
    end_latitude = models.FloatField(default=0.0)
    end_longitude = models.FloatField(default=0.0)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'team : {} ,user_id: {}'.format(
            self.team, self.user_id)


class JoinedClasses(models.Model):
    video_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250, default='non')
    user_department = models.CharField(max_length=250, default='non')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'video_id : {}'.format(
            self.video_id)


class GroupedPerformance(models.Model):
    """User combined performance"""
    pass
