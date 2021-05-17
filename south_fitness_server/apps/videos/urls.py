from django.urls import path
from .views import (Videos, VideoAllView, VideoSpecificView, VideoAdmin,
                    TokenGenerator, VideoTrainerSpecific, DateRequest)

urlpatterns = [
    path('',
         Videos.as_view(),
         name="Videos"
         ),

    path('trainer/<uploader_id>',
         VideoTrainerSpecific.as_view(),
         name="trainer_videos"
         ),

    path('<video_id>',
         VideoSpecificView.as_view(),
         name="specific_video"
         ),

    path('all/<yester_date>',
         VideoAllView.as_view(),
         name="all_videos from today"
         ),

    path('admin/all/',
         VideoAdmin.as_view(),
         name="all_videos"
         ),

    path('access_token/',
         TokenGenerator.as_view(),
         name="Generate Token"
         ),

    path('date_request/<date>',
         DateRequest.as_view(),
         name="Date request"
         )
]
