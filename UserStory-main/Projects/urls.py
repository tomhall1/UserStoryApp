from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('list/', views.Projects_list, name='Projects'),
    path('AddProject/', views.add_Projects, name='AddProject'),
    path('projectDetails/<int:id>', views.projectDetails, name='projectDetails')
]
