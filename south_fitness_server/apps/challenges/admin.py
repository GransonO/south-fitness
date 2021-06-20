from django.contrib import admin
from .models import MvtChallenge, JoinedClasses, ExtraChallenges

# Register your models here.

admin.site.register(MvtChallenge)
admin.site.register(JoinedClasses)
admin.site.register(ExtraChallenges)
