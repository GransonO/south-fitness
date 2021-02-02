from django.urls import path
from .views import (Notifications, NotificationAllView,
                    NotificationSpecificView, NotificationUserView)

urlpatterns = [
    path('',
         Notifications.as_view(),
         name="notifications"
         ),

    path('<notification_id>',
         NotificationSpecificView.as_view(),
         name="specific_notifications"
         ),

    path('user/<user_id>',
         NotificationUserView.as_view(),
         name="specific_notifications"
         ),

    path('all/',
         NotificationAllView.as_view(),
         name="all_notifications"
         )
]
