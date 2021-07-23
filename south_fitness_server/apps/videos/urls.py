from django.urls import path
from .views import (Videos, VideoAllView, VideoSpecificView, VideoAdmin, History, VideoUpdate, ActivitiesTrainerSpecific,
                    TokenGenerator, VideoTrainerSpecific, DateRequest, Participants, ActivityUpdate,
                    Activities, ActivitiesAllView, ActivitiesAdmin, ActivitiesSpecificView)

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

    path('update/',
         VideoUpdate.as_view(),
         name="Update video"
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
         ),

    # Activities
    path('activities/',
         Activities.as_view(),
         name="Activity"
         ),

    path('activities/update/',
         ActivityUpdate.as_view(),
         name="Update Activities"
         ),

    path('activities/<uploader_id>',
         ActivitiesTrainerSpecific.as_view(),
         name="trainer_videos"
         ),

    path('specific/<video_id>',
         ActivitiesSpecificView.as_view(),
         name="specific_video"
         ),

    path('activities/all/',
         ActivitiesAllView.as_view(),
         name="all_videos from today"
         ),

    path('admin/all/',
         ActivitiesAdmin.as_view(),
         name="all_videos"
         ),

    path('participants/',
         Participants.as_view(),
         name="all_videos"
         ),

    path('history/',
         History.as_view(),
         name="User History"
         ),
]
