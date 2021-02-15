from django.db import models


class TeamsDB(models.Model):

    teams_id = models.CharField(
        unique=True, max_length=250, default='non')
    team_name = models.CharField(max_length=250, default='non')
    slogan = models.CharField(max_length=1050, default='non')
    image = models.CharField(max_length=250, default='non')
    created_by = models.CharField(max_length=1050, default='non')
    is_active = models.BooleanField(default=False)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'team_name : {} ,slogan: {}'.format(
            self.team_name, self.slogan)
