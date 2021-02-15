from django.urls import path
from .views import (Test, Teams, TeamsAllView,
                    TeamsSpecificView, TeamsUserView)

urlpatterns = [
    path('',
         Test.as_view(),
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

    path('all/',
         TeamsAllView.as_view(),
         name="all_support"
         )
]
