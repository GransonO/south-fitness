from django.urls import path
from .views import (Videos, VideoAllView, VideoSpecificView,
                    TokenGenerator, VideoTrainerSpecific)

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

    path('all/',
         VideoAllView.as_view(),
         name="all_videos"
         ),

    path('access_token/',
         TokenGenerator.as_view(),
         name="Generate Token"
         )
]
