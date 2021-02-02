from django.contrib import admin
from .models import (Accounts, DoctorAccount, WithdrawalAccount)

# Register your models here.

admin.site.register(Accounts)
admin.site.register(DoctorAccount)
admin.site.register(WithdrawalAccount)
