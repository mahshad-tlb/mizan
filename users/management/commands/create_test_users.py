
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'ایجاد 10 کاربر تستی'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        for i in range(10):
            username = f'testuser{i}'
            email = f'testuser{i}@example.com'
            password = 'testpassword123'

            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'✅ user {username} was created.'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ کاربر {username} از قبل وجود دارد.'))
