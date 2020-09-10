from django.urls import path
from .views import FcmRecord, UserFcmRecord

urlpatterns = [
    path('',
         FcmRecord.as_view(),
         name="fcm_records"
         ),
     path('<user_id>',
         UserFcmRecord.as_view(),
         name="user_fcm_records"
         ),
]
