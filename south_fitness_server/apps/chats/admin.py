from django.contrib import admin
from .models import ChatDB
from .models import GroupsDB

# Register your models here.

admin.site.register(ChatDB)
admin.site.register(GroupsDB)
