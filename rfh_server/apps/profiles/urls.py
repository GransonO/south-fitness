from django.urls import path
from .views import (ProfileRef)

urlpatterns = [
#     path('',
#          Profiles.as_view(),
#          name="profiles"
#          ),

#     path('all/',
#          ProfilesAllView.as_view(),
#          name="all_profiles"
#          ),

    path('ref/',
         ProfileRef.as_view(),
         name="all_profiles"
         )
]
