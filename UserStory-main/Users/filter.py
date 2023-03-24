import django_filters
from django import forms
from UserStoryApp.models import User


class UsersFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search place', 'id': 'nameInput', 'class': 'form-control filter'}))

    class Meta:
        model = User
        fields = ['username', 'Role']
