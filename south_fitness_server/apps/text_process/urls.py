from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.Processing.as_view(),
        name='process'),

]
