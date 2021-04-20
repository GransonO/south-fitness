from django.urls import path
from .views import (
     Profiles, ProfileInstitutionSpecific,
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

    path('institution/<institution>',
         ProfileInstitutionSpecific.as_view(),
         name="Specific institution profiles"
         ),

    path('all/',
         ProfilesAllView.as_view(),
         name="all profiles"
         )
]
