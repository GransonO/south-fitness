from django.urls import path
from .views import FcmRecord, UserFcmRecord, AllFcmRecords

urlpatterns = [
    path('',
         FcmRecord.as_view(),
         name="fcm_records"
         ),
     path('<user_id>',
         UserFcmRecord.as_view(),
         name="user_fcm_records"
         ),
     path('all/',
         AllFcmRecords.as_view(),
         name="all_fcm_records"
         ),
]
