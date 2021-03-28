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

from .apps.notifications import urls as notificationUrls
from .apps.support import urls as supportUrls
from .apps.profiles import urls as profilesUrls
from .apps.fcm import urls as fcmUrls
from .apps.staff import urls as staffUrls
from .apps.authentication import urls as authUrls
from .apps.videos import urls as videoUrls
from .apps.teams import urls as teamsUrls
from .apps.blogs import urls as blogsUrls
from .apps.challenges import urls as challengeUrls
from .apps.chats import urls as chatUrls

urlpatterns = [
    path('admin/', admin.site.urls),

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
        'videos/',
        include(videoUrls),
        name="videos"),

    path(
        'staff/',
        include(staffUrls),
        name="staff"),

    path(
        'auth/',
        include(authUrls),
        name="authentication"),

    path(
        'team/',
        include(teamsUrls),
        name="teams"),

    path(
        'blog/',
        include(blogsUrls),
        name="blog"),

    path(
        'challenge/',
        include(challengeUrls),
        name="challenges"),

    path(
        'chats/',
        include(chatUrls),
        name="chats"),
]
