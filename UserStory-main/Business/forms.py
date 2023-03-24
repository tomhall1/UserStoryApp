from django import forms
from UserStoryApp.models import BusinessCategory, Business, User


class MyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class UserMyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.username


class AddBusinessForm1(forms.Form):
    name = forms.CharField(widget=forms.Textarea(
        attrs={"rows": "2", "class": "bg-gray form-control col-6"}))
    hourlyRate = forms.IntegerField(widget=forms.NumberInput(
        attrs={"rows": "2", "class": "bg-gray form-control col-6"}))
    # LegalEntityName = forms.CharField()
    # Address = forms.CharField()
    # BusinessNumber = forms.IntegerField()
    # BusinessEmail = forms.CharField()


class AddBusinessForm2(forms.Form):
    LegalEntityName = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"rows": "2", "class": "bg-gray form-control col-6"}))
    Address = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"rows": "2", "class": "bg-gray form-control col-6"}))
    BusinessNumber = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs={"rows": "2", "class": "bg-gray form-control col-6"}))
    BusinessEmail = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"rows": "2", "class": "bg-gray form-control col-6"}))
    ABN = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs={"rows": "2", "class": "bg-gray form-control col-6"}))
