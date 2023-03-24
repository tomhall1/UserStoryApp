from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('removeUserStory/<int:id>', views.del_userStroy, name='del'),
    path('relatedUserStory',
         views.related_userStory, name='relatedUserStories'),
    path('editPersona/<int:id>', views.editPersona, name='editPersona'),
    path('addPersona/<int:id>', views.addPersona, name='editPersona'),
    path('addDevTask/<int:id>', views.addDevTask, name='editPersona'),
    path('editDevTask/<int:id>', views.editDevTask, name='editDevTask'),
    path('editRaids/<int:id>', views.editRaids, name='editRaids'),
    path('addRaids/<int:id>', views.addRaids, name='addRaids'),
    path('editUserStory/<int:id>', views.editUserStory, name='editUserStory'),
    path('editEstimate/<int:id>', views.editEstimate, name='editEstimate'),
    path('addEstimate/<int:id>', views.addEstimate, name='addEstimate'),
    path('editProject/<int:id>', views.editProject, name='editProject'),
    path('editUserStoryVersion/<int:id>',
         views.editUserStoryVersion, name='editUserStoryVersion'),
    path('addUserStory/<int:id>',
         views.addUserStory, name='addUserStory'),
    path('getAllfilters', views.getAllfilters, name='getAllfilters'),
    path('addUserStory',
         views.addNewUserStory, name=''),
    path('addPlatform',
         views.addPlatform, name='addPlatform'),
    path('addIndustry',
         views.addIndustry, name='addIndustry'),
    path('addSelectedUserStory/<int:id>',
         views.addSelectedUserStory, name='addSelectedUserStory'),
    path('RemoveField',
         views.RemoveField, name='RemoveField')
]
