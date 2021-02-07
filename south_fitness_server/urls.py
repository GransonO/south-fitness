"""south_fitness_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from .apps.text_process import urls as process_urls
from .apps.mpesa import urls as mpesaUrls
from .apps.appointments import urls as appointmentUrls
from .apps.notifications import urls as notificationUrls
from .apps.support import urls as supportUrls
from .apps.profiles import urls as profilesUrls
from .apps.fcm import urls as fcmUrls
from .apps.staff import urls as staffUrls
from .apps.accounts import urls as accountsUrls
from .apps.authentication import urls as authUrls

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'text_process/',
        include(process_urls),
        name='process'),

    path(
        'mpesa_callback/',
        include(mpesaUrls),
        name="mpesaUrls"),

    path(
        'appointments/',
        include(appointmentUrls),
        name="appointments"),

    path(
        'notifications/',
        include(notificationUrls),
        name="notifications"),

    path(
        'support/',
        include(supportUrls),
        name="support"),

    path(
        'profiles/',
        include(profilesUrls),
        name="profiles"),

    path(
        'fcm/',
        include(fcmUrls),
        name="fcm"),

    path(
        'staff/',
        include(staffUrls),
        name="staff"),

    path(
        'accounts/',
        include(accountsUrls),
        name="accounts"),

    path(
        'auth/',
        include(authUrls),
        name="authentication"),
]