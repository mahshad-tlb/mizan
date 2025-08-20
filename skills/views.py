from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
from .utils import ensure_user_skill_file
from django.http import FileResponse, Http404
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
import os

@login_required
def skills_table(request):
    """
    نمایش جدول مهارت‌ها
    """
    usf = ensure_user_skill_file(request.user)
    df = pd.read_excel(usf.file.path)

    # استانداردسازی ستون‌ها
    df.columns = [str(c).strip() for c in df.columns]
    df = df.rename(columns={k: v for k, v in {
        'Skill': 'Skill', 'skill': 'Skill', 'skills': 'Skill', 'مهارت': 'Skill',
        'Score': 'Score', 'score': 'Score', 'امتیاز': 'Score'
    }.items() if k in df.columns})

    df["Score"] = pd.to_numeric(df["Score"], errors="coerce").fillna(0)
    max_score = float(df["Score"].max() or 1)
    df["ScorePercent"] = (df["Score"] / max_score * 100).clip(0, 100).round(2)

    skills_data = df.to_dict(orient='records')
    return render(request, 'table.html', {
        'skills': skills_data,
        'max_score': max_score
    })


@login_required
def update_skill(request, skill_id):
    """
    افزایش یا کاهش امتیاز مهارت و ذخیره دائمی در اکسل
    همچنین ارسال ایمیل به سوپر‌یوزرها
    (روش بدون JSON/JS)
    """
    usf = ensure_user_skill_file(request.user)
    df = pd.read_excel(usf.file.path)

    # استانداردسازی ستون‌ها
    df.columns = [str(c).strip() for c in df.columns]
    df = df.rename(columns={k: v for k, v in {
        'Skill': 'Skill', 'skill': 'Skill', 'skills': 'Skill', 'مهارت': 'Skill',
        'Score': 'Score', 'score': 'Score', 'امتیاز': 'Score'
    }.items() if k in df.columns})

    df["Score"] = pd.to_numeric(df["Score"], errors="coerce").fillna(0)

    if request.method == "POST":
        # دریافت delta از فرم
        try:
            delta = int(request.POST.get("delta", 0))
        except ValueError:
            delta = 0

        # بررسی skill_id معتبر (توجه: skill_id باید از 0 تا len(df)-1 باشد)
        if 0 <= skill_id < len(df):
            df.loc[df.index[skill_id], "Score"] += delta

        # محاسبه درصد
        max_score = df["Score"].max() if df["Score"].max() > 0 else 1
        df["ScorePercent"] = (df["Score"] / max_score * 100).clip(0, 100).round(2)

        # ذخیره دائمی
        df.to_excel(usf.file.path, index=False)

        # ارسال ایمیل به سوپر‌یوزرها
        User = get_user_model()
        superusers = User.objects.filter(is_superuser=True)
        for su in superusers:
            if su.email:
                email = EmailMessage(
                    subject=f"Skill file updated for {request.user.username}",
                    body=f"کاربر {request.user.username} فایل مهارت‌های خود را به‌روز کرد.",
                    to=[su.email]
                )
                email.attach_file(usf.file.path)
                email.send(fail_silently=False)

    # بعد از POST یا GET، جدول بروزرسانی شده را نشان بده
    skills_data = df.to_dict(orient='records')
    return render(request, 'table.html', {
        'skills': skills_data,
        'max_score': df["Score"].max() if df["Score"].max() > 0 else 1
    })


@login_required
def download_user_skill(request, filename):
    """
    دانلود فایل اکسل مهارت کاربر
    """
    file_path = os.path.join(settings.MEDIA_ROOT, 'user_skills', filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        raise Http404("File not found")
