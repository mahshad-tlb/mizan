from django import forms
from django_pwned_passwords.validators import PwnedPasswordsValidator
from django.contrib.auth.hashers import make_password
from users.models import SecondaryPassword

class SecondaryPasswordForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[PwnedPasswordsValidator()],
        label="رمز دوم"
    )

    class Meta:
        model = SecondaryPassword
        fields = ['password']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        # رمز رو هش می‌کنیم
        instance.password = make_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance
