from django.urls import path
from .views import Register, Login, ResetPass

urlpatterns = [
    path("register",
         Register.as_view(),
         name="Register"
         ),
    path("login",
         Login.as_view(),
         name="Login"
         ),
    path("reset",
         ResetPass.as_view(),
         name="ResetPass"
         ),
]
