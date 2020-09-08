from django.urls import path
from .views import AppointmentsViews, AppointmentState, AppointmentSpecificView

urlpatterns = [
    path('',
         AppointmentsViews.as_view(),
         name="appointments"
         ),
    path('state/',
         AppointmentState.as_view(),
         name="appointmentState"
         ),
    path(
        'user/<user_id>',
        AppointmentSpecificView.as_view(),
        name='appointmentSpecific'),
]
