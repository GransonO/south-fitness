from django.urls import path
from .views import (
    Challenges, TodayChallenges, Participants,
    ChallengesAllView, ChallengeSpecificView,
    AllRegisteredActivities, ChallengesGetAll)

urlpatterns = [
    path('',
         Challenges.as_view(),
         name="Challenges"
         ),

    path('<user_id>',
         ChallengeSpecificView.as_view(),
         name="specific Challenge"
         ),

    path('all/',
         ChallengesAllView.as_view(),
         name="all Challenges"
         ),

    path('today/<user_id>',
         TodayChallenges.as_view(),
         name="Today Challenges"
         ),

    path('join/',
         AllRegisteredActivities.as_view(),
         name="join Challenges"
         ),

    path('join/user/<user_id>',
         AllRegisteredActivities.as_view(),
         name="join Challenges"
         ),

    path('joined/<challenge_id>',
         ChallengesGetAll.as_view(),
         name="All members in Challenges"
         ),

    path('members/',
         Participants.as_view(),
         name="Members in Challenge"
         )
]
