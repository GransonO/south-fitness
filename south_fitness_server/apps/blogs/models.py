from django.db import models


class BlogsDB(models.Model):
    """Blog DB"""

    blog_id = models.CharField(unique=True, max_length=250)
    uploaded_by = models.CharField(max_length=250, default='non')
    uploader_id = models.CharField(max_length=250, default='non')
    title = models.CharField(max_length=250, default='non')
    body = models.CharField(max_length=5050, default='non')
    image_url = models.CharField(max_length=1050, default='non')
    views_count = models.IntegerField(default=0)
    reading_duration = models.CharField(max_length=250, default='10 mins')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'title : {}'.format(
            self.title)
