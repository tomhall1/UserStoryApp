from django import forms
from UserStoryApp.models import Role, User


class AddUserForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-100'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-100'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-100'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-100'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-100'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-100'}))
    Role = forms.TypedChoiceField(choices=[(choice.value, choice.name)
                                           for choice in Role], widget=forms.Select(attrs={'class': 'form-control form-select'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'password', 'email', 'Role']

    def clean(self):
        cleaned_data = super(AddUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-100'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-100'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-100'}))
    Update_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-100'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-100'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-100'}))
    Role = forms.TypedChoiceField(choices=[(choice.value, choice.name)
                                           for choice in Role], widget=forms.Select(attrs={'class': 'form-control form-select'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'Update_password', 'confirm_password', 'email', 'Role']

    def clean(self):
        cleaned_data = super(EditUserForm, self).clean()
        password = cleaned_data.get("Update_password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

    def save(self, commit=True):
        account = super(EditUserForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email']
        account.first_name = self.cleaned_data['first_name']
        account.last_name = self.cleaned_data['last_name']
        account.Role = self.cleaned_data['Role']
        if commit:
            account.save()
        return account
