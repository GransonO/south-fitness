from django.urls import path
from .views import (Teams, TeamsAllView,
                    TeamsSpecificView, TeamsUserView)

urlpatterns = [
    path('',
         Teams.as_view(),
         name="teams"
         ),

    path('<support_id>',
         TeamsSpecificView.as_view(),
         name="specific_support"
         ),

    path('user/<user_id>',
         TeamsUserView.as_view(),
         name="specific_user_support"
         ),

    path('all',
         TeamsAllView.as_view(),
         name="all_support"
         )
]
