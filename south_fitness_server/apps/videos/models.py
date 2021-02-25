from django.db import models


class VideosDB(models.Model):

    video_id = models.CharField(unique=True, max_length=250)
    uploaded_by = models.CharField(max_length=250, default='non')
    instructor = models.CharField(max_length=250, default='non')
    title = models.CharField(max_length=250, default='non')
    details = models.CharField(max_length=1050, default='non')
    video_url = models.CharField(max_length=1050, default='non')
    image_url = models.CharField(max_length=1050, default='non')
    views_count = models.IntegerField(default=0)
    type = models.CharField(max_length=250, default='non')
    session_id = models.CharField(max_length=250, default='non')
    isScheduled = models.BooleanField(default=False)
    scheduledTime = models.DateTimeField(null=True)
    isComplete = models.BooleanField(default=False)
    isLive = models.BooleanField(default=False)

    participants = models.CharField(max_length=5000, null=True)

    video_call_id = models.CharField(max_length=5000, null=True)
    video_call_token = models.CharField(max_length=5000, null=True)
    video_channel_name = models.CharField(max_length=5000, null=True)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'title : {} ,type: {}'.format(
            self.title, self.type)
