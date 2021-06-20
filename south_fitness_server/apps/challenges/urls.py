from django.urls import path
from .views import (
    Challenges, TodayChallenges, Participants,
    ChallengesAllView, ChallengeSpecificView,
    ListedChallenge, GetListedChallenge)

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

    path('members/',
         Participants.as_view(),
         name="Members in Challenge"
         ),

    path('listed/',
         ListedChallenge.as_view(),
         name="The Listed Challenges"
         ),

    path('listed/all/',
         GetListedChallenge.as_view(),
         name="All Listed Challenges"
         )


]
