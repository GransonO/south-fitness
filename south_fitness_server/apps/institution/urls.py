from django.urls import path
from .views import Institution, AllInstitutions

urlpatterns = [
    path('',
         Institution.as_view(),
         name="Institution"
         ),

    path('all/',
         AllInstitutions.as_view(),
         name="AllInstitutions"
         ),
]
