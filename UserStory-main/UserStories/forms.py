from django import forms


class AddUserStoryForm(forms.Form):
    iWantTO = forms.CharField()
    soThat = forms.CharField()
    priority = forms.CharField()
