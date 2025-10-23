"""
Django settings for mlsite project — listo para despliegue en Render.

Más info:
https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables desde .env si existen
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# 🔐 Seguridad
# =========================

# Usa la variable de entorno en producción
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-$yf_g&bdmd+3ub^v5!_gg)cg0wjum1gwxj$b(cke+yuf)!!hd2')

# Cambia DEBUG con variable de entorno para evitar dejarlo en True en producción
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Importante: agregar dominio de Render
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "insurance-diabetes.onrender.com"
]

# =========================
# 📦 Aplicaciones
# =========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.ml',  # Tu app personalizada
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Muy importante para servir archivos estáticos correctamente en producción:
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mlsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'mlsite.wsgi.application'

# =========================
# 🗄️ Base de Datos
# =========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# (Opcional) Si luego usas PostgreSQL en Render, podrías leer DATABASE_URL desde os.getenv()

# =========================
# 🔑 Validación de contraseñas
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# 🌐 Internacionalización
# =========================

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# =========================
# 🧾 Archivos estáticos
# =========================

STATIC_URL = '/static/'

# Carpeta donde Django guardará los archivos recolectados en producción
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Carpetas adicionales que contengan archivos estáticos en desarrollo
STATICFILES_DIRS = [
    BASE_DIR / 'apps' / 'ml' / 'static',
]

# Whitenoise permite servir archivos estáticos directamente en Render sin Nginx
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =========================
# ⚙️ Configuración adicional
# =========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}