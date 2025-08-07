from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
import random

from users.models import Users, SMSVerificationCode
from users.forms.verification_forms import PhoneNumberForm, CodeVerificationForm
from users.utils.sms import send_verification_code
import logging
logger = logging.getLogger('users.sms')

def send_code_view(request):
    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            code = str(random.randint(100000, 999999))
            cleaned_phone=f'+98{phone}'
            logger.debug(f"Phone number received for verification: {cleaned_phone}")
            # ذخیره یا به‌روزرسانی کد
            SMSVerificationCode.objects.update_or_create(
                phone_number=cleaned_phone,
                defaults={'code': code, 'created_at': timezone.now()}
            )
            logger.info(f"Verification code saved/updated for {cleaned_phone}")

            # ارسال پیامک
            send_verification_code(cleaned_phone, code)
            logger.info(f"Verification code sent via SMS to {cleaned_phone}")

            request.session['phone_number'] = cleaned_phone
            logger.debug(f"Phone number {cleaned_phone} stored in session")
            messages.success(request, "کد تایید ارسال شد.")
            return redirect('verify_code')
    else:
        form = PhoneNumberForm()
        logger.debug("Phone number form rendered.")
    return render(request, 'send_code.html', {'form': form})



def verify_code_view(request):
    phone = request.session.get('phone_number')
    if not phone:
        logger.warning("Attempt to verify code without phone number in session.")
        messages.error(request, "ابتدا شماره موبایل را وارد کنید.")
        return redirect('send_code')

    if request.method == "POST":
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            logger.debug(f"User submitted verification code: {code} for phone {phone}")

            try:
                verification = SMSVerificationCode.objects.get(phone_number=phone, code=code)
                logger.info(f"Correct verification code entered for phone {phone}")
            except SMSVerificationCode.DoesNotExist:
                logger.warning(f"Invalid verification code {code} for phone {phone}")
                messages.error(request, "کد وارد شده نادرست است.")
                return render(request, "verify_code.html", {"form": form})

            if verification.is_expired():
                logger.warning(f"Verification code for phone {phone} is expired.")
                messages.error(request, "کد منقضی شده است.")
                return render(request, "verify_code.html", {"form": form})

            try:
                user = Users.objects.get(phone_number=phone)
                request.session['user_id'] = user.id
                logger.info(f"User {user.username} logged in via SMS verification.")
                verification.delete()
                logger.debug(f"Verification code for {phone} deleted after successful login.")
                return redirect("home")

            except Users.DoesNotExist:
                logger.warning(f"No user found with phone number {phone}")
                messages.error(request, "کاربری با این شماره یافت نشد.")
    else:
        form = CodeVerificationForm()
        logger.debug("Code verification form rendered.")

    return render(request, "verify_code.html", {"form": form})
