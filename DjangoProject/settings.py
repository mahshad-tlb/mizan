import os
from pathlib import Path
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
TIME_ZONE = ZoneInfo("Asia/Tehran")


# 📥 Load environment variables from .env
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")
# 🔐 Security
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1']
ALLOWED_HOSTS = ['*']
# 📦 Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',


    'users',
    'comments.apps.CommentsConfig',
    'uploads',

    'storages',
    'ckeditor',
    'sections',
    'adminsortable2'
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
    'users.middleware.rate_limit_middleware.RedisRateLimitMiddleware',
    'allauth.account.middleware.AccountMiddleware',

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
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoProject.wsgi.application'

# 🛢️ Database
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'local')


if ENVIRONMENT == 'production':
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('DB_ENGINE'),
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT'),
        }
    }
else:
    # لوکال با SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / os.environ.get('SQLITE_DB_NAME', 'db.sqlite3'),
        }
    }

# 🔐 Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# 🖼️ Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# 🗝️ Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ☁️ Arvan Storage settings
ARVAN_ACCESS_KEY = os.environ.get('ARVAN_ACCESS_KEY')
ARVAN_SECRET_KEY = os.environ.get('ARVAN_SECRET_KEY')
ARVAN_BUCKET = os.environ.get('ARVAN_BUCKET')
ARVAN_ENDPOINT = os.environ.get('ARVAN_ENDPOINT')

# 📨 Email settings
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ['true', '1']
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False').lower() in ['true', '1']
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# 🔐 Google OAuth
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = "https://mtlb.erfann31dev.ir/auth/google/callback/"


# ⚙️ Django AllAuth
SITE_ID = 5
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',

)

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
LOGIN_REDIRECT_URL = '/home'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}
SOCIALACCOUNT_ADAPTER = 'users.adapters.CustomSocialAccountAdapter'

# 📲 SMS.IR Settings
SMS_IR_SECRET_KEY = os.environ.get('SMS_IR_SECRET_KEY')
SMS_IR_TEMPLATE_ID = os.environ.get('SMS_IR_TEMPLATE_ID')
SMS_IR_LINE_NUMBER = os.environ.get('SMS_IR_LINE_NUMBER')

# 🧠 Redis cache (for rate limiting)
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = int(os.environ.get('REDIS_DB', 0))

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# 📝 Logging
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

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

PASSWORD_RESET_TIMEOUT =60 * 60 * 24