from django.urls import path
from .views import (
     Staff, StaffAllView, StaffSpecificEmail,
     StaffSpecificView, StaffState, StaffDoctorsView,
     AllAvailableDocs
     )

urlpatterns = [
    path('',
         Staff.as_view(),
         name="staff"
         ),

    path('<staffID>',
         StaffSpecificView.as_view(),
         name="specific profiles"
         ),

    path('all/',
         StaffAllView.as_view(),
         name="all staff"
         ),

    path('state/',
         StaffState.as_view(),
         name="staff state"
         ),

    path('email/<staff_email>',
         StaffSpecificEmail.as_view(),
         name="specific email"
         ),

    path('doctors/',
         StaffDoctorsView.as_view(),
         name="all doctors"
         ),

    path('avail/',
         AllAvailableDocs.as_view(),
         name="Available doctors"
         ),
]
