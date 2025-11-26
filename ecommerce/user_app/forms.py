from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=200, label="username")
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # Validations
    def clean(self):
        cleaned_data = super().clean()
        usrnm=cleaned_data.get('username')
        pwd = cleaned_data.get('password')
        cpwd = cleaned_data.get('confirm_password')

        if pwd != cpwd:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Hashing Password
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user