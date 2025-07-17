from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, label="نام کاربری")
    password= forms.CharField(widget=forms.PasswordInput, label="رمز عبور")
    phone_number = forms.CharField(max_length=12, label="شماره تماس")
    email = forms.EmailField(label="ایمیل")


class SignupForm(forms.Form):
    username = forms.CharField(label="نام کاربری", max_length=15)
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    email = forms.EmailField(label="ایمیل")
    phone_number = forms.CharField(label="شماره همراه", max_length=15)

class EmailForm(forms.Form):
    email = forms.EmailField(label="ایمیل")

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="ایمیل", widget=forms.EmailInput(attrs={'placeholder': 'ایمیل خود را وارد کنید'}))

class NewPasswordForm(forms.Form):
    new_password = forms.CharField(label="رمز عبور جدید", widget=forms.PasswordInput)