from django.db import models


class VideosDB(models.Model):

    video_id = models.CharField(unique=True, max_length=550)
    uploaded_by = models.CharField(max_length=250, default='non')
    uploader_id = models.CharField(max_length=350, default='non')
    instructor = models.CharField(max_length=250, default='non')
    title = models.CharField(max_length=250, default='non')
    details = models.CharField(max_length=1050, default='non')
    video_url = models.CharField(max_length=1050, default='non')
    image_url = models.CharField(max_length=1050, default='non')
    views_count = models.IntegerField(default=0)
    type = models.CharField(max_length=550, default='non')
    session_id = models.CharField(max_length=550, default='non')
    duration = models.CharField(max_length=250, default='10 mins')
    isScheduled = models.BooleanField(default=False)
    scheduledTime = models.TimeField(null=True)
    scheduledDate = models.DateField(null=True)
    isComplete = models.BooleanField(default=False)
    isLive = models.BooleanField(default=False)

    participants = models.CharField(max_length=5000, default='non')

    video_call_id = models.CharField(max_length=5000, null=True)
    video_call_token = models.CharField(max_length=5000, null=True)
    video_channel_name = models.CharField(max_length=5000, null=True)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'title : {} ,type: {}'.format(
            self.title, self.type)


class VidsARatings(models.Model):
    activity_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250, default='non')
    user_department = models.CharField(max_length=250, default='non')
    username = models.CharField(max_length=250, default='non')
    trainer_rating = models.FloatField(default=0.0)
    activity_rating = models.FloatField(default=0.0)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'activity_id : {}'.format(
            self.activity_id)


class ActivitiesDB(models.Model):

    activity_id = models.CharField(unique=True, max_length=550)
    uploaded_by = models.CharField(max_length=250, default='non')
    uploader_id = models.CharField(max_length=350, default='non')
    title = models.CharField(max_length=250, default='non')
    details = models.CharField(max_length=1050, default='non')
    video_url = models.CharField(max_length=1050, default='non')
    image_url = models.CharField(max_length=1050, default='non')
    type = models.CharField(max_length=550, default='non')
    session_id = models.CharField(max_length=550, default='non')
    sets = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    duration_ext = models.CharField(max_length=15, default="1 Week")
    level = models.CharField(max_length=15, default="Beginner")
    equip = models.CharField(max_length=250, default="Minimum")
    isComplete = models.BooleanField(default=False)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'title : {} ,type: {}'.format(
            self.title, self.type)


class JoinedVidsActs(models.Model):
    activity_id = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250, default='non')
    user_department = models.CharField(max_length=250, default='non')
    username = models.CharField(max_length=250, default='non')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'activity_id : {}'.format(
            self.activity_id)
