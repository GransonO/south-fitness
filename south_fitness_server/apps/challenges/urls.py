from django.urls import path
from .views import (
    Challenges,
    ChallengesAllView, ChallengeSpecificView
     )

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
         )
]
