from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from allauth.account.utils import user_email

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        email = user_email(user)

        # اطمینان از وجود EmailAddress
        email_address, created = EmailAddress.objects.get_or_create(
            user=user,
            email=email,
            defaults={"primary": True, "verified": False}
        )

        # ارسال ایمیل تأیید حتی اگر EmailAddress قبلاً وجود داشته
        confirmation = EmailConfirmationHMAC(email_address)
        confirmation.send(request)

        return user
