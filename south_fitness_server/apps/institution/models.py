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
    institute_logo = models.CharField(max_length=1250, default='https://res.cloudinary.com/dolwj4vkq/image/upload/v1627289273/South_Fitness/insitutions/logo.png')
    is_active = models.BooleanField(default=True)

    institute_img1 = models.CharField(max_length=1250, default='https://res.cloudinary.com/dolwj4vkq/image/upload/v1627461186/South_Fitness/insitutions/legUp.png')
    institute_img2 = models.CharField(max_length=1250, default='https://res.cloudinary.com/dolwj4vkq/image/upload/v1627461186/South_Fitness/insitutions/legUp.png')
    institute_img3 = models.CharField(max_length=1250, default='https://res.cloudinary.com/dolwj4vkq/image/upload/v1627461186/South_Fitness/insitutions/legUp.png')

    institute_message1 = models.CharField(max_length=1250, default='Message 1')
    institute_message2 = models.CharField(max_length=1250, default='Message 2')
    institute_message3 = models.CharField(max_length=1250, default='message 3')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'institute_name : {} ,institute_admin: {}'.format(
            self.institute_name, self.institute_admin_name)
