from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
import random

from users.models import Users, SMSVerificationCode
from users.forms.verification_forms import PhoneNumberForm, CodeVerificationForm
from users.utils.sms import send_verification_code


def send_code_view(request):
    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            code = str(random.randint(100000, 999999))
            cleaned_phone=f'+98{phone}'
            # ذخیره یا به‌روزرسانی کد
            SMSVerificationCode.objects.update_or_create(
                phone_number=cleaned_phone,
                defaults={'code': code, 'created_at': timezone.now()}
            )

            # ارسال پیامک
            send_verification_code(cleaned_phone, code)

            request.session['phone_number'] = cleaned_phone
            messages.success(request, "کد تایید ارسال شد.")
            return redirect('verify_code')
    else:
        form = PhoneNumberForm()
    return render(request, 'send_code.html', {'form': form})



def verify_code_view(request):
    phone = request.session.get('phone_number')
    if not phone:
        messages.error(request, "ابتدا شماره موبایل را وارد کنید.")
        return redirect('send_code')

    if request.method == "POST":
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']

            try:
                verification = SMSVerificationCode.objects.get(phone_number=phone, code=code)
            except SMSVerificationCode.DoesNotExist:
                messages.error(request, "کد وارد شده نادرست است.")
                return render(request, "verify_code.html", {"form": form})

            if verification.is_expired():
                messages.error(request, "کد منقضی شده است.")
                return render(request, "verify_code.html", {"form": form})

            try:
                user = Users.objects.get(phone_number=phone)
                request.session['user_id'] = user.id
                verification.delete()
                return redirect("home")
            except Users.DoesNotExist:
                messages.error(request, "کاربری با این شماره یافت نشد.")
    else:
        form = CodeVerificationForm()

    return render(request, "verify_code.html", {"form": form})
