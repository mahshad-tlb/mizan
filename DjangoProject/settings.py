from pathlib import Path
import os

# 📁 Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Security
SECRET_KEY = 'django-insecure-&8j7olto2(it_wh-5!+ry_)jok+d7)x!p)$x$@r&_be$sj5xic'
DEBUG = True
ALLOWED_HOSTS = []

# 📦 Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # اپلیکیشن‌های پروژه
    'users',
    'comments.apps.CommentsConfig',
    'uploads',

    # سایر کتابخانه‌ها
    'storages',
    'ckeditor',
]

# 🧠 Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # ⚠️ ریت لیمیت بعد از احراز هویت اضافه شود
    'users.middleware.rate_limit_middleware.RedisRateLimitMiddleware',
]

# 🔗 URL Configuration
ROOT_URLCONF = 'DjangoProject.urls'

# 🎨 Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoProject.wsgi.application'

# 🛢️ Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔐 Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'django_pwned_passwords.validators.PwnedPasswordsValidator',
    },
]

# 🌍 Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 🖼️ Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# 🗝️ Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 📧 Email backend (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ☁️ Arvan Storage settings
ARVAN_ACCESS_KEY = '1cec986f-9ea5-4d56-ab11-ff7b041679d2'
ARVAN_SECRET_KEY = '823fdc456a2720ff59071f5af61c3766227cebf2ca565d1b46bee71d98c8a1a4'
ARVAN_BUCKET = 'mahshad'
ARVAN_ENDPOINT = 'https://s3.ir-thr-at1.arvanstorage.ir'

# 📜 Logging
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)  # اطمینان از وجود پوشه

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file_secondary_password': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'secondary_password.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'second_pass': {
            'handlers': ['file_secondary_password'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

# 🚦 Redis cache for rate limiting
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6380/1",  # مطمئن شو Redis اجرا شده
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
