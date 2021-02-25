from django.urls import path
from .views import (
     Blog,
     BlogAllView, BlogSpecificView
     )

urlpatterns = [
    path('',
         Blog.as_view(),
         name="Blog"
         ),

    path('<blog_id>',
         BlogSpecificView.as_view(),
         name="Specific Blogs"
         ),

    path('all/',
         BlogAllView.as_view(),
         name="All Blogs"
         )
]
