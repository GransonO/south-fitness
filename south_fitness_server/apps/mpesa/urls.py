from django.urls import path
from .views import MpesaCallback

urlpatterns = [
    path('',
         MpesaCallback.as_view(),
         name="MpesaCallback"
         ),
]
