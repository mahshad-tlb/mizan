from django import forms

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="ایمیل", widget=forms.EmailInput(attrs={'placeholder': 'ایمیل خود را وارد کنید'}))

class NewPasswordForm(forms.Form):
    new_password = forms.CharField(label="رمز عبور جدید", widget=forms.PasswordInput)
