from pathlib import Path
import os
from datetime import timedelta

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Load .env manually ---
env_path = BASE_DIR / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())
else:
    raise Exception("⚠️ .env file not found at backend/.env")

# --- Security ---
SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1")

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "d1b4b7e3a561.ngrok-free.app",
    "0a454e7b366c.ngrok-free.app",
    "99e4adbd0611.ngrok-free.app",
]

# Dynamically allow any ngrok subdomain in development
if DEBUG:
    import re
    class RegexList(list):
        def __contains__(self, key):
            return any(re.fullmatch(pattern, key) for pattern in self)
    ALLOWED_HOSTS = RegexList(ALLOWED_HOSTS + [r"[a-z0-9\-]+\.ngrok\-free\.app"])

# --- Application definition ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    # Your apps
    "cart",
    "orders",
    "products",
    "users",
    "contact",
    "payments",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "backend.wsgi.application"

# --- Database ---
DATABASES = {
    "default": {
        "ENGINE": os.environ["DB_ENGINE"],  # e.g., "django.db.backends.postgresql"
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# --- Password validation ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internationalization ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static & Media ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- Primary Key Field ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- REST Framework ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

# --- Custom User ---
AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = [
    "users.api.backends.CustomAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# --- CORS ---
CORS_ALLOWED_ORIGINS = [
    "https://marzok16.github.io",
    "http://localhost:5173",
    "http://localhost:5174",
    "https://99e4adbd0611.ngrok-free.app",
    "https://amazon-clone-store.loca.lt",
    "https://my-amazon-store.loca.lt",
    "https://short-puma-32.loca.lt",
    "http://192.168.1.44:5173"
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_METHODS = [
    "DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept", "accept-encoding", "authorization", "content-type",
    "dnt", "origin", "user-agent", "x-csrftoken", "x-requested-with",
    "ngrok-skip-browser-warning",
]

# Allow media files to be accessed from any origin
CORS_URLS_REGEX = r'^/(api|media)/.*$'

# Add CORS headers to media files
CORS_EXPOSE_HEADERS = [
    "content-type",
    "content-length",
    "cache-control",
    "expires",
    "last-modified",
    "etag",
]

# --- JWT ---
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.environ.get("JWT_ACCESS_LIFETIME", 10))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.environ.get("JWT_REFRESH_LIFETIME", 60))),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
}

# --- Email ---
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# --- Frontend ---
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")

# --- Stripe ---
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
