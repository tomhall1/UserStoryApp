from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('list/', views.userStories_list, name='userStories'),
    path('addUserStory/', views.add_userStory, name='addUserStory'),
    path('userStoryDetails/<int:id>',
         views.Details, name='userStoryDetails'),
    path('userStoryEdit/<int:id>',
         views.userStoryDetails, name='Edit')
]
