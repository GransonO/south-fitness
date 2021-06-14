from django.contrib import admin
from .models import MvtChallenge, JoinedClasses, JoinedActivities, ExtraActivities

# Register your models here.

admin.site.register(MvtChallenge)
admin.site.register(JoinedClasses)
admin.site.register(JoinedActivities)
admin.site.register(ExtraActivities)
