from django.db import models


class ChatDB(models.Model):

    message_id = models.CharField(unique=True, max_length=250, default='non')
    group_id = models.CharField(max_length=250, default='non')
    user_id = models.CharField(max_length=250, default='non')
    message = models.CharField(max_length=1000, default='non')
    username = models.CharField(max_length=250, default='non')
    reply_body = models.CharField(max_length=550)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'message_id : {} ,message: {}'.format(
            self.message_id, self.message)


class GroupsDB(models.Model):

    group_id = models.CharField(unique=True, max_length=250, default='non')
    created_by = models.CharField(max_length=250, default='non')
    group_title = models.CharField(max_length=250, default='non')
    group_slogan = models.CharField(max_length=250, default='non')
    creator_name = models.CharField(max_length=250, default='non')
    is_closed = models.BooleanField(default=False)
    channel_id = models.CharField(max_length=250, default='non')
    group_image = models.CharField(max_length=550, default='non')
    isVerified = models.BooleanField(default=False)
    institution = models.CharField(max_length=100, default='SOUTH_FITNESS')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'group_id : {} ,group_title: {}'.format(
            self.group_id, self.group_title)


class GeneralGroupMembers(models.Model):
    alias = models.CharField(default=None, max_length=250,)
    user_id = models.CharField(unique=True, max_length=250,)
    email = models.CharField(unique=True, max_length=250,)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'alias : {} ,user_id: {}'.format(
            self.alias, self.user_id)
