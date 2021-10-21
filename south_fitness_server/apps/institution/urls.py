from django.urls import path
from .views import Institution, AllInstitutions, SpecificInstitutions, AddTheAdmin

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

    path('admin/',
         AddTheAdmin.as_view(),
         name="Add The Admin"
         ),
]
