from django.urls import path
from .views import (
     ProfileRef, Profiles,
     ProfilesAllView, ProfileSpecificView
     )

urlpatterns = [
    path('',
         Profiles.as_view(),
         name="profiles"
         ),

    path('<userId>',
         ProfileSpecificView.as_view(),
         name="specific profiles"
         ),

    path('all/',
         ProfilesAllView.as_view(),
         name="all profiles"
         ),

    path('ref/',
         ProfileRef.as_view(),
         name="refs"
         )
]
