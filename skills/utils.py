from pathlib import Path
from django.conf import settings
import shutil
from .models import UserSkillFile
from uuid import uuid4


DEFAULT_XLSX = Path(settings.BASE_DIR) / 'data' / 'gozaresh.xlsx'

def ensure_user_skill_file(user) -> UserSkillFile:

    obj, created = UserSkillFile.objects.get_or_create(user=user, defaults={'file': ''})
    if not obj.file:
        dest_dir = Path(settings.MEDIA_ROOT) / 'user_skills'
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / f'{user.pk}_{uuid4().hex}.xlsx'
        shutil.copy(DEFAULT_XLSX, dest_path)

        obj.file.name = f'user_skills/{dest_path.name}'
        obj.save()
    return obj
