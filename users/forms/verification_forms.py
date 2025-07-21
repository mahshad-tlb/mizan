from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(label="ایمیل")

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label="شماره موبایل")

class CodeVerificationForm(forms.Form):
    code = forms.CharField(max_length=10, label="کد تایید")
