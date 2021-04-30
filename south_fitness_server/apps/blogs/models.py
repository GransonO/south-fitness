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
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    reading_duration = models.CharField(max_length=250, default='10 mins')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'title : {}'.format(
            self.title)


class Comments(models.Model):
    """Blog Comments"""
    blog_id = models.CharField(max_length=250)
    username = models.CharField(max_length=250, default='non')
    uploader_id = models.CharField(max_length=250, default='non')
    profile_image = models.CharField(
        max_length=550,
        default='https://res.cloudinary.com/dolwj4vkq/image/upload/v1619738022/South_Fitness/user.png')
    body = models.CharField(max_length=5050, default='non')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'username : {}'.format(
            self.username)
