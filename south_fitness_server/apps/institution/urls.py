from django.urls import path
from .views import Institution, AllInstitutions, SpecificInstitutions

urlpatterns = [
    path('',
         Institution.as_view(),
         name="Institution"
         ),

    path('<institute_id>',
         SpecificInstitutions.as_view(),
         name="Specific Institution"
         ),

    path('all/',
         AllInstitutions.as_view(),
         name="AllInstitutions"
         ),
]
