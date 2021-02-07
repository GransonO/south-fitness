from django.urls import path
from .views import (
     Profiles,
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
         )
]
