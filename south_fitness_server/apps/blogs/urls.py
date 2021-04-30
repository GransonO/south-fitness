from django.urls import path
from .views import (
     Blog, BlogsTrainerSpecific,
     BlogAllView, BlogSpecificView,
     BlogComments, AllBlogComments
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

    path('trainer/<uploader_id>',
         BlogsTrainerSpecific.as_view(),
         name="Trainer Blogs"
         ),

    path('all/',
         BlogAllView.as_view(),
         name="All Blogs"
         ),

    path('comments/',
         BlogComments.as_view(),
         name="Post Comments"
         ),

    path('comments/all/',
         AllBlogComments.as_view(),
         name="Post Comments"
         )
]
