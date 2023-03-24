from django import forms
from UserStoryApp.models import Business


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class AddProjectsForm(forms.Form):
    business = MyModelChoiceField(queryset=Business.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control'}))
    Name_of_Project = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
