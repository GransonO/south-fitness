from django.urls import path
from .views import Notifications

urlpatterns = [
    path('',
         Notifications.as_view(),
         name="notifications"
         )
]
