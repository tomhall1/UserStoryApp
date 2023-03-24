from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('list/', views.business_list, name='Business'),
    path('AddBusiness/', views.add_business, name='AddBusiness'),
    path('BusinessDetails/<int:id>', views.BusinessDetails, name='BusinessDetails')
]
