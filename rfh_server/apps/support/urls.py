from django.urls import path
from .views import (Support, SupportAllView,
                    SupportSpecificView, SupportUserView)

urlpatterns = [
    path('',
         Support.as_view(),
         name="support"
         ),

    path('<support_id>',
         SupportSpecificView.as_view(),
         name="specific_support"
         ),

    path('user/<user_id>',
         SupportUserView.as_view(),
         name="specific_user_support"
         ),

    path('all/',
         SupportAllView.as_view(),
         name="all_support"
         )
]
