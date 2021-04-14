from django.urls import path
from .views import (Videos, VideoAllView, VideoSpecificView, TokenGenerator)

urlpatterns = [
    path('',
         Videos.as_view(),
         name="Videos"
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
