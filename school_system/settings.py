import os
from pathlib import Path
from dotenv import load_dotenv

# ===== プロジェクトのルートディレクトリを取得 =====
BASE_DIR = Path(__file__).resolve().parent.parent

LOGIN_URL = '/users/login/'

# ===== .env ファイルのロード =====
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ .env file loaded from {env_path}")
else:
    print("⚠️ .env file not found! Please create one.")

# ===== 環境変数の取得（デフォルト値あり） =====
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "default-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in ("true", "1", "yes")
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ===== デバッグ用出力（本番環境では非表示推奨） =====
print(f"🔍 DEBUG = {DEBUG}")
print(f"🔍 SECRET_KEY = {SECRET_KEY[:10]}********")  # 秘密鍵の漏洩防止
print(f"🔍 DATABASE_NAME = {os.getenv('DATABASE_NAME', 'Not Set')}")
print(f"🔍 DATABASE_USER = {os.getenv('DATABASE_USER', 'Not Set')}")
print(f"🔍 DATABASE_HOST = {os.getenv('DATABASE_HOST', 'Not Set')}")
print(f"🔍 EMAIL_HOST_USER = {os.getenv('EMAIL_HOST_USER', 'Not Set')}")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',  # ✅ tasks アプリ
    'users',  # ✅ users アプリ (ない場合は追加する)
    'dm',
    'calendarapp',  
    'notes',      # ノート機能用
    'lessons',  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.LoginHistoryMiddleware',
]

ROOT_URLCONF = 'school_system.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # ここが空になっていないか確認！
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'school_system.wsgi.application'

# ===== データベース設定 =====
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'school_system_db',
        'USER': 'postgres',
        'PASSWORD': 'tIUnct4i', 
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# ===== 認証とパスワードバリデーション =====
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===== 言語・タイムゾーン設定 =====
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'

# ✅ Django が `static/` を探せるようにする
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===== カスタムユーザーモデル =====
AUTH_USER_MODEL = 'users.CustomUser'

# ===== メール設定（SMTP） =====
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False").lower() in ("true", "1", "yes")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "default@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "default_password")

# ===== セキュリティ対策 =====
SECURE_BROWSER_XSS_FILTER = True  # XSS（クロスサイトスクリプティング）対策
SECURE_CONTENT_TYPE_NOSNIFF = True  # ブラウザによるMIMEタイプの誤認防止
SESSION_COOKIE_HTTPONLY = True  # クライアント側のJSによるアクセスを制限
CSRF_COOKIE_HTTPONLY = True  # CSRFトークンをJSからアクセス不能にする
X_FRAME_OPTIONS = 'DENY'  # iframe埋め込みを防止
SECURE_HSTS_SECONDS = 31536000  # HSTS（HTTPS強制）を1年間適用
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ===== ロギング設定（エラーを記録） =====
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# ===== デフォルトのプライマリーキー =====
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GOOGLE_CREDENTIALS_FILE = os.path.join(BASE_DIR, 'google_credentials.json')
# その他、必要な設定（カレンダーIDなど）も追加可能
GOOGLE_CALENDAR_ID = 'your_calendar_id@group.calendar.google.com'
# school_system/settings.py の末尾付近
LOGOUT_REDIRECT_URL = '/users/login/'

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_default_api_key')