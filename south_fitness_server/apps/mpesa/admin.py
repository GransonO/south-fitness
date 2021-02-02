from django.contrib import admin
from .models import MpesaEntryModel, MpesaEntryDB

# Register your models here.

admin.site.register(MpesaEntryModel)
admin.site.register(MpesaEntryDB)
