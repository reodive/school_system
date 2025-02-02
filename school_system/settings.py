import os
from pathlib import Path
from dotenv import load_dotenv

# プロジェクトのルートディレクトリを取得
BASE_DIR = Path(__file__).resolve().parent.parent

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

# ✅ 環境変数を取得（デフォルト値あり）
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "default-secret-key")

# ✅ 環境変数で DEBUG を管理（環境変数が "True" の場合のみ有効）
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"

# ✅ デバッグ用（環境変数の値を出力して確認）
print(f"🔍 DEBUG = {DEBUG}")
print(f"🔍 SECRET_KEY = {SECRET_KEY[:10]}********")  # 長いキーを隠す
print(f"🔍 DATABASE_USER = {os.getenv('DATABASE_USER')}")
print(f"🔍 EMAIL_HOST_USER = {os.getenv('EMAIL_HOST_USER')}")

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# アプリケーション定義
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # APIサポート
    'users',
    'tasks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'school_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ✅ テンプレートフォルダを指定
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

WSGI_APPLICATION = 'school_system.wsgi.application'

# ✅ データベース設定（環境変数から取得）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DATABASE_NAME", "school_system_db"),
        'USER': os.getenv("DATABASE_USER", "default_user"),
        'PASSWORD': os.getenv("DATABASE_PASSWORD", "default_password"),
        'HOST': os.getenv("DATABASE_HOST", "localhost"),
        'PORT': os.getenv("DATABASE_PORT", "5432"),
    }
}

# パスワードバリデーション
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ 日本時間に設定
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True
USE_TZ = True

# 静的ファイル（CSS, JS, 画像）
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# メディアファイル（アップロード用）
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# カスタムユーザーモデル
AUTH_USER_MODEL = 'users.CustomUser'

# ✅ メール設定（環境変数を利用）
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "default@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "default_password")

# ✅ デフォルトのプライマリーキー
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
