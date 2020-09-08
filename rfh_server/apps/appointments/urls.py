from django.urls import path
from .views import AppointmentsViews, AppointmentState

urlpatterns = [
    path('',
         AppointmentsViews.as_view(),
         name="appointments"
         ),
    path('state/',
         AppointmentState.as_view(),
         name="appointmentState"
         ),
]
