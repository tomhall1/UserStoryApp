from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('list/', views.user_list, name='users'),
    path('addUser/', views.add_user, name='addUsers'),
    path('userDetails/<int:id>', views.userDetails, name='userDetails')
]
