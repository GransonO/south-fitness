from django.urls import path
from .views import (Chat, ChatsAllView, InstitutionGroups, RegisterGeneralMember,
                    ChatSpecificView, Groups, GroupsAllView, AllGroups)

urlpatterns = [
    path('',
         Chat.as_view(),
         name="Chat"
         ),

    path('<message_id>',
         ChatSpecificView.as_view(),
         name="specific_message"
         ),

    path('all/<group_id>',
         ChatsAllView.as_view(),
         name="all_chats"
         ),

    path('groups/',
         Groups.as_view(),
         name="create_groups"
         ),

    path('all_groups/',
         AllGroups.as_view(),
         name="All_Groups"
         ),

    path('groups/all/',
         GroupsAllView.as_view(),
         name="GroupsAllView"
         ),

    path('groups/all/<institute>',
         InstitutionGroups.as_view(),
         name="InstitutionGroups"
         ),

    path('general/',
         RegisterGeneralMember.as_view(),
         name="RegisterGeneralMember"
         )


]
