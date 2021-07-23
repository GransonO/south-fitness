from django.db import models

# Create your models here.


class Institutions(models.Model):
    institute_id = models.CharField(
        unique=True, max_length=250, default='non')
    institute_name = models.CharField(max_length=250, default='non')
    institute_admin_name = models.CharField(max_length=250, default='non')
    institute_admin_email = models.CharField(max_length=250, default='non')
    institute_primary_color = models.CharField(max_length=250, default='non')
    institute_secondary_color = models.CharField(max_length=250, default='non')
    institute_logo = models.CharField(max_length=1250, default='non')
    is_active = models.BooleanField(default=True)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'institute_name : {} ,institute_admin: {}'.format(
            self.institute_name, self.institute_admin_name)
