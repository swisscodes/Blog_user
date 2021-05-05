from django import forms
from account.models import CustomUserModel


class LoginForm(forms.Form):
    username = forms.CharField(label="Login with Email or Username")
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUserModel
        fields = ("email", "username", "first_name")

        help_texts = {
            "email": ("Required. Valid email only"),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]
