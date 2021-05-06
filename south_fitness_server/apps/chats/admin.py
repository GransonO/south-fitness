from django.contrib import admin
from .models import ChatDB
from .models import GroupsDB
from .models import GeneralGroupMembers

# Register your models here.

admin.site.register(ChatDB)
admin.site.register(GroupsDB)
admin.site.register(GeneralGroupMembers)
