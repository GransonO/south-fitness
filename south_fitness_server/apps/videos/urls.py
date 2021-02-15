from django.urls import path
from .views import (Videos, VideoAllView, VideoSpecificView)

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
         )
]
