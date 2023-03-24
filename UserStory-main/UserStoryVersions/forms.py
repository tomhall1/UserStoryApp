from django import forms
from UserStoryApp.models import Project


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class AddUserStoryVersionForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    projects = MyModelChoiceField(queryset=Project.objects.all())
