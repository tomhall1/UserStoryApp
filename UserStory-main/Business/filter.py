import django_filters
from django import forms
from UserStoryApp.models import Business


class BusinessFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='gt', widget=forms.TextInput(attrs={
        'placeholder': 'Search place', 'class': 'form-control filter'}))

    class Meta:
        model = Business
        fields = ['name']
