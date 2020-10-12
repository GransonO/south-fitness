from django.urls import path
from .views import (AppointmentsViews,
                    AppointmentState, AppointmentDoctorSpecific,
                    AppointmentSpecificView, AppointmentGeneralView,
                    EmergencyView, EmergencyStateView)

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

    path(
        'doctors/<doctorID>',
        AppointmentDoctorSpecific.as_view(),
        name='AppointmentDoctorSpecific'),

    path(
        'all/',
        AppointmentGeneralView.as_view(),
        name='AppointmentGeneralView'),

    path(
        'sos/',
        EmergencyView.as_view(),
        name='EmergencyView'),

    path(
        'sos/state/',
        EmergencyStateView.as_view(),
        name='EmergencyStateView'),
]
