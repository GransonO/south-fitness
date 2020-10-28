from django.urls import path
from .views import Accounts

urlpatterns = [
    path(
        '',
        Accounts.as_view(),
        name='Accounts'),

]
