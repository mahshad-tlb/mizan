from django import forms
from django.contrib.auth.hashers import make_password
from users.models import SecondaryPassword  # اطمینان حاصل کن این مدل در users/models.py هست
from pwned_passwords_django.validators import PwnedPasswordsValidator
from django.core.exceptions import ValidationError





class SignupForm(forms.Form):
    username = forms.CharField(label="نام کاربری", max_length=15)
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    secondary_password = forms.CharField(label="رمز دوم", widget=forms.PasswordInput)
    email = forms.EmailField(label="ایمیل")
    phone_number = forms.CharField(label="شماره همراه", max_length=20)

    def clean_secondary_password(self):
        password = self.cleaned_data.get("secondary_password")
        validator = PwnedPasswordsValidator()
        try:
            validator.validate(password)
        except ValidationError:
            raise forms.ValidationError("رمز دوم ناامن است و قبلاً لو رفته! لطفاً رمز قوی‌تری وارد کنید.")
        return password

    def save(self, user):
        """
        این متد باید در view مربوطه فراخوانی شود،
        بعد از ساختن کاربر اصلی
        """
        secondary_password = self.cleaned_data.get("secondary_password")
        if secondary_password:
            SecondaryPassword.objects.create(
                user=user,
                password=make_password(secondary_password)
            )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, label="نام کاربری")
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")
